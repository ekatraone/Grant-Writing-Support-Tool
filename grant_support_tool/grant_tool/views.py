from django.shortcuts import render, redirect, get_object_or_404
from .models import GrantDraft
from .forms import GrantDraftForm
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download necessary NLTK resources
nltk.download("vader_lexicon")

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")
sia = SentimentIntensityAnalyzer()

def home(request):
    if request.method == 'POST':
        form = GrantDraftForm(request.POST)
        if form.is_valid():
            draft = form.save()
            content = draft.content

            # Analyze content
            analysis_results = analyze_content(content)

            # Store analysis results in the model
            draft.analysis_results = analysis_results
            draft.save()

            return redirect('results', pk=draft.pk)
    else:
        form = GrantDraftForm()

    return render(request, 'grant_tool/home.html', {'form': form})


def analyze_content(content):
    """
    Analyze the grant content for grammar issues and sentiment.
    """

    # Analyze grammar using spaCy
    doc = nlp(content)
    grammar_issues = []
    for token in doc:
        if token.is_alpha and token.tag_ in ['MD', 'VBZ', 'VBP']:  # Example tags
            grammar_issues.append(f"Issue with word: '{token.text}' (Part of speech: {token.tag_})")

    # Analyze sentiment using NLTK
    sentiment_scores = sia.polarity_scores(content)
    sentiment = (
        f"Positive: {sentiment_scores['pos']}, "
        f"Negative: {sentiment_scores['neg']}, "
        f"Neutral: {sentiment_scores['neu']}, "
        f"Overall: {'Positive' if sentiment_scores['compound'] > 0 else 'Negative'}"
    )

    # Combine grammar and sentiment results
    feedback = (
        "Grammar Issues:\n" + "\n".join(grammar_issues) +
        f"\n\nSentiment Analysis:\n{sentiment}"
    )

    return feedback


def results(request, pk):
    """
    Display the results of the analysis.
    """
    draft = get_object_or_404(GrantDraft, pk=pk)
    return render(request, 'grant_tool/results.html', {'draft': draft})
