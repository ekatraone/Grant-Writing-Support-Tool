from flask import Flask, render_template, request
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from werkzeug.utils import secure_filename
import docx
import pdfplumber
import re

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the pre-trained model and tokenizer
model_name = "gpt2"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

# Function to parse documents
def parse_document(file_path):
    text = ""
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    elif file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    return text.strip()

# Function to extract sections from text
def extract_sections(text):
    sections = {
        "Introduction": "",
        "Statement of Need": "",
        "Project Goals and Objectives": "",
        "Methods": "",
        "Budget": ""
    }
    
    # Define regex patterns for each section
    patterns = {
        "Introduction": r"(Introduction|Overview|Background)(.*?)(?=(Statement of Need|Project Goals and Objectives|Methods|Budget|$))",
        "Statement of Need": r"(Statement of Need|Need|Problem Statement|Justification)(.*?)(?=(Introduction|Project Goals and Objectives|Methods|Budget|$))",
        "Project Goals and Objectives": r"(Project Goals and Objectives|Goals|Objectives|Aims)(.*?)(?=(Introduction|Statement of Need|Methods|Budget|$))",
        "Methods": r"(Methods|Methodology|Approach)(.*?)(?=(Introduction|Statement of Need|Project Goals and Objectives|Budget|$))",
        "Budget": r"(Budget|Costs|Financial Plan)(.*?)(?=(Introduction|Statement of Need|Project Goals and Objectives|Methods|$))"
    }
    
    # Extract sections based on patterns
    for section, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[section] = match.group(2).strip()
    
    return sections

# Function to generate grant proposal text
def generate_grant_proposal(documents, keywords):
    input_text = " ".join(documents) + " Keywords: " + ", ".join(keywords) + ". Draft a grant proposal based on this information."
    
    # Tokenize 
    inputs = tokenizer.encode(input_text, return_tensors="pt", padding=True, truncation=True)
    # Create an attention mask
    attention_mask = (inputs != tokenizer.pad_token_id).long()
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_new_tokens=500,  # Set the maximum number of new tokens to generate
            pad_token_id=tokenizer.eos_token_id,  # Set pad_token_id to eos_token_id
            attention_mask=attention_mask  # Pass the attention mask
        )
    
    proposal = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Split the proposal into sentences
    sentences = proposal.split('. ')
    
    # Divide sentences into three paragraphs
    num_sentences = len(sentences)
    if num_sentences < 3:
        # If there are fewer than 3 sentences, just return the original proposal
        formatted_proposal = proposal.replace('. ', '.\n\n')
    else:
        # Calculate the number of sentences per paragraph
        sentences_per_paragraph = num_sentences // 3
        paragraphs = []
        
        for i in range(3):
            start_index = i * sentences_per_paragraph
            if i == 2:  # For the last paragraph, take all remaining sentences
                end_index = num_sentences
            else:
                end_index = start_index + sentences_per_paragraph
            
            paragraph = '. '.join(sentences[start_index:end_index]).strip() + '.'
            paragraphs.append(paragraph)
        
        # Join paragraphs with double new lines
        formatted_proposal = '\n\n'.join(paragraphs)

    return formatted_proposal

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        documents = []
        # Handle file uploads
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    documents.append(parse_document(file_path))
        
        # Handle text input
        text_documents = request.form.getlist("documents")
        documents.extend(text_documents)

        # Extract sections from the combined documents
        combined_text = " ".join(documents)
        extracted_sections = extract_sections(combined_text)

        # Prepare keywords for proposal generation
        keywords = request.form.get("keywords").split(",")
        proposal = generate_grant_proposal(documents, keywords)

        return render_template("index.html", proposal=proposal, sections=extracted_sections)
    return render_template("index.html", proposal=None, sections=None)

if __name__ == "__main__":
    app.run(debug=True)