import streamlit as st
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import openai

#openai api key
OPENAI_API_KEY = "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"

# Hugging Face API Configuration
HUGGINGFACE_API_TOKEN = "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"
HUGGINGFACE_MODEL = "EleutherAI/gpt-neo-1.3B"

HUGGINGFACE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# MIstral
MISTRAL_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"

# Hugging Face API Function
def call_huggingface_gptneo(prompt):
    try:
        payload = {
        "inputs": prompt,
        "parameters": {
        "max_length": 1024,  # Shorter response
        "temperature": 0.8,  # Moderate creativity
        "top_p": 0.8,  # Reduce randomness
        "do_sample": True,
    },
        }
        response = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("generated_text", "No response received.")
    except requests.exceptions.RequestException as e:
        return f"Hugging Face API Error: {str(e)}"

# Load GPT-Neo Model and Tokenizer
@st.cache_resource
def load_model():
    model_name = "EleutherAI/gpt-neo-1.3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

# Generate text using the local GPT-Neo model
def generate_text(prompt, max_length=1024, temperature=0.8, top_p=0.9):
    tokenizer, model = load_model()
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        temperature=temperature,
        top_p=top_p,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

def call_openai(prompt, api_key, model="gpt-3"):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        return f"OpenAI Error: {str(e)}"

# MISTRAL API Function
def call_mistral(prompt):
    try:
        payload = {
        "inputs": prompt,
        "parameters": {
        "max_length": 2048,  # Shorter response
        "temperature": 0.8,  # Moderate creativity
        "top_p": 0.8,  # Reduce randomness
        "do_sample": True,
    },
        }
        response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()

         # Hugging Face response structure is a list of dictionaries
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, list) and "text" in result[0]:
            return result[0]["text"]
        else:
            return "No response received from Mistral API."
        
        #return result.get("generated_text", "No response received.")
    except requests.exceptions.RequestException as e:
        return f"Hugging Face API Error: {str(e)}"
    
def load_mistral_local(user_prompt):
    try:
        # Load the model and tokenizer
        model_name = "mistralai/Mistral-7B-v0.1"

        print("Loading tokenizer and model... This might take a while if not cached.")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remote_code=True)

        # Initialize a text generation pipeline
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")

        # Generate text
        print("Generating text...")
        output = generator(
            user_prompt,
            max_length=128,  # Limit the response length
            do_sample=True,  # Sampling for creativity
            temperature=0.7,  # Moderate creativity
            top_p=0.9,  # Nucleus sampling to control randomness
            truncation = True,
            pad_token_id=tokenizer.eos_token_id
        )

        # Return the generated text
        return output[0]["generated_text"]

    except Exception as e:
        return f"Error: {str(e)}"
    


# Streamlit UI
st.title("Grant Writing Proposal Tool")

# Project Idea Input
idea_text = st.text_input("Enter your project idea:", placeholder="E.g., Write a grant for ASL Model detection.")

# Project Goal Input
goals_text = st.text_input("Enter your project goal:", placeholder="E.g., Facilitate communication without a translator.")

# Model Selection
model_option = st.radio("Choose a text generation model:", ("OpenAI GPT", "Hugging Face", "Mistral"))

if model_option == 'Hugging Face':
    model1 = st.radio("Choose option for creating Grant:", ("Hugging Face Local", "Hugging Face API"))

if model_option == 'Mistral':
    model2 = st.radio("Choose option for creating Grant:", ("Mistral Local", "Mistral API"))


# Generate Proposal Button
if st.button("Generate Proposal"):
    if not idea_text or not goals_text:
        st.warning("Please fill in both fields before generating!")
    else:
        with st.spinner("Generating your grant proposal..."):
            # Create the user prompt
            user_prompt = (
                f"Write a 500-word grant proposal for the following project:\n\n"
                f"Project Idea: {idea_text}\n"
                f"Goals to Achieve: {goals_text}\n\n"
                f"Include the following sections:\n"
                f"1. Project Abstract: A concise summary\n"
                f"2. Statement of Need\n"
                f"3. Project Description\n"
                f"4. Goals and Objectives\n"
                f"5. Timeline\n"
                f"6. Budget\n"
                f"7. Evaluation\n"
                f"8. Conclusion"
            )

            # Call the selected model
            if model_option == 'OpenAI GPT':
               response = call_openai(user_prompt, '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')
                
            if model_option == 'Hugging Face':
                if model1 == 'Hugging Face API':
                    response = call_huggingface_gptneo(user_prompt)
                else: 
                    response =  generate_text(user_prompt)

            if model_option == 'Mistral':
                if model2 == 'Mistral API':
                    response = call_mistral(user_prompt)
                else: 
                    response =  load_mistral_local(user_prompt)

        # Display the Generated Proposal
        st.success("Grant Proposal Generated!")
        st.text_area("Generated Proposal:", value=response, height=2000)
