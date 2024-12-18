# Grant Proposal Generator (using Documents and Keywords)
This is a web application built using Flask and Hugging Face's GPT-2 model to help generate grant proposals based on uploaded documents and keywords. The application allows users to upload .txt, .docx, and .pdf files, extract key sections from these documents, and generate a draft grant proposal.

#### Features
Document Upload: Upload .txt, .docx, and .pdf files.
Text Extraction: Extracts text from the uploaded documents.
Section Extraction: Identifies and extracts key sections from the document like "Introduction", "Statement of Need", "Project Goals and Objectives", "Methods", and "Budget".
Grant Proposal Generation: Generates a draft grant proposal using the GPT-2 language model based on the extracted text and user-provided keywords.
Web Interface: A simple web interface to upload files and provide additional input.

#### Requirements
Python 3.7+
Flask
PyTorch
Hugging Face's transformers library
pdfplumber
python-docx
werkzeug

#### Installation and Steps:
1. Clone the Repository
2. Create a Virtual Environment
3. Install Dependencies
4. Download the Pre-trained Model

1. Running the Application
To start the application, run the following command:
bash
Copy code
python app.py
This will start a local development server. You can access the application in your browser at http://127.0.0.1:5000/.

2. Using the Web Interface
File Upload: Click the "Choose Files" button to upload .txt, .docx, or .pdf files.
Text Input: You can also directly input text or documents in the provided text boxes.
Keywords: Provide a list of keywords (separated by commas) that the generated proposal should incorporate.
Generate Proposal: After uploading the files and entering keywords, click the "Generate Proposal" button to receive the grant proposal and extracted sections displayed below.

### File Structure
grant-proposal-generator/
│
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # HTML template for rendering the web interface
├── uploads/            # Directory for uploaded files
│
└── Readme.md           # This file

### How It Works
Document Parsing: The app allows you to upload .txt, .docx, or .pdf files. It extracts text from these documents using respective libraries: docx for .docx files and pdfplumber for .pdf files.
Section Extraction: The extracted text is analyzed for specific sections (e.g., Introduction, Budget, etc.) using regular expressions. This helps break down the document into key sections for the grant proposal.
Proposal Generation: After extracting text and sections from the uploaded documents, the application uses the GPT-2 model to generate a grant proposal. The proposal is generated based on the content and keywords provided.
User Interface: The Flask web application handles the user interaction. The user can upload files, input additional text, and keywords, and then view the generated proposal on the web page.

#### Customization
Model: The application uses the GPT-2 model (gpt2), but you can replace this with other models from Hugging Face's model hub (e.g., gpt-neo or gpt-3).
Text Processing: The section extraction logic is based on regular expressions. You can modify the regex patterns in the extract_sections function to better suit your needs (e.g., for different types of grant proposals).

#### Troubleshooting
Model Loading Issues: If the model fails to load or generate output, ensure that the correct dependencies (PyTorch, Transformers, etc.) are installed and that you have an active internet connection to download the model.
File Upload Errors: If you're unable to upload or process files, ensure that the uploaded files are in the correct format (.txt, .docx, .pdf).
Performance: The proposal generation might take some time, especially with large documents or if you're running the application on limited hardware. Try reducing the document size or keywords to improve performance.

![image](https://github.com/user-attachments/assets/82fd12a1-5a60-40e5-bea2-36558328d9e9)



