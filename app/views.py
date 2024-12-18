import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from transformers import pipeline, DistilBertForSequenceClassification, DistilBertTokenizerFast
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr

# Sentiment Analysis Setup
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)

# Sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Label mapping for sentiment analysis
label_mapping = {
    'LABEL_0': 'negative',
    'LABEL_1': 'neutral',
    'LABEL_2': 'positive'
}

# Sentiment Analysis View
@csrf_exempt
def analyze_text(request):
    if request.method == 'POST':
        try:
            # Parse input text
            input_data = json.loads(request.body)
            input_text = input_data.get('text', '')

            if not input_text:
                return JsonResponse({'error': 'No text provided'}, status=400)

            # Perform sentiment analysis
            result = sentiment_pipeline(input_text)

            # Debugging: Print the raw output from the pipeline
            print(f"Raw result: {result}")  # Debugging output

            if result and isinstance(result, list) and 'label' in result[0]:
                label = result[0]['label']
                score = result[0]['score']

                # Confidence is the score (already between 0 and 1)
                confidence = round(score * 100, 2)  # Ensure confidence is a percentage

            else:
                label = 'unknown'
                confidence = 0  # No valid score

            # Map the label to sentiment
            sentiment = label_mapping.get(label, 'unknown')

            # Return the analysis as JSON
            return JsonResponse({
                'analysis': {
                    'label': sentiment,
                    'confidence': confidence  # Return confidence as percentage
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Voice Note Transcription View
@csrf_exempt
def transcribe_voice_note(request):
    if request.method == 'POST':
        try:
            recognizer = sr.Recognizer()
            audio_file = request.FILES.get('audio')

            # Recognize the audio file
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)

            return JsonResponse({'transcribed_text': text})

        except Exception as e:
            return JsonResponse({'error': 'An error occurred while processing the audio.'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Other views (if needed)
def index(request):
    return render(request, 'index.html')

def analyze_page(request):
    return render(request, 'analyze.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def resources(request):
    return render(request, 'resources.html')
