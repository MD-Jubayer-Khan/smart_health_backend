# File: health_portal/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .data_collector import fetch_medlineplus_topics, fetch_openfda_matches
from suggestify import QuerySuggester
import spacy
import wikipedia

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ------------------ Helper Functions ------------------

def extract_main_entity(query: str) -> str:
    """Extract the main medical entity from query using spaCy."""
    doc = nlp(query)
    entities = [ent.text for ent in doc.ents if ent.label_ in ["DISEASE", "SYMPTOM"]]
    if entities:
        return entities[0]
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    return noun_chunks[-1] if noun_chunks else query

def detect_intent(query: str) -> str:
    """Detect intent in the query to modify Wikipedia search."""
    query_lower = query.lower()
    if any(kw in query_lower for kw in ["what should i do", "how to treat", "treatment for"]):
        return "treatment"
    if any(kw in query_lower for kw in ["how to prevent", "prevention", "avoid"]):
        return "prevention"
    if "symptom" in query_lower or "symptoms" in query_lower:
        return "description"
    return "general"

def fetch_wiki_summary(term: str, sentences: int = 3) -> str:
    """Fetch Wikipedia summary for a term."""
    try:
        summary = wikipedia.summary(term, sentences=sentences, auto_suggest=True, redirect=True)
        return summary
    except Exception:
        return f"Sorry currently no data available for '{term}'."

# ------------------ Health Info Endpoint with Suggestions ------------------

@api_view(["GET"])
def get_health_info(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return Response({"error": "Query parameter 'q' is required."})

    #  Extract main entity
    main_entity = extract_main_entity(query)

    #  Detect intent
    intent = detect_intent(query)

    #  Build Wikipedia search term
    if intent == "treatment":
        wiki_term = f"{main_entity} treatment"
    elif intent == "prevention":
        wiki_term = f"{main_entity} prevention"
    else:
        wiki_term = main_entity

    #  Fetch educational content
    wiki_summary = fetch_wiki_summary(wiki_term)
    educational_content = [
        {
            "title": wiki_term,
            "source": "Wikipedia",
            "summary": wiki_summary
        }
    ]

    #  Generate related topic suggestions using Suggestify
    all_terms = [main_entity] + [c['title'] for c in educational_content]
    suggester = QuerySuggester(data_source=all_terms, use_wiki=False)
    related_topics = suggester.suggest(query, top_k=5)

    response_data = {
        "query": query,
        "main_entity": main_entity,
        "intent": intent,
        "educational_content": educational_content,
        "related_topics": related_topics
    }

    return Response(response_data)


# ------------------ Suggestion Endpoint ------------------
@api_view(['GET'])
def suggestions(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({"suggestions": []})

    data = fetch_medlineplus_topics(query) + fetch_openfda_matches(query)
    if not data:
        data = ["Headache", "Fever", "Cough", "Vomiting", "Fatigue"]

    suggester = QuerySuggester(data_source=data, use_wiki=False)
    suggestions_list = suggester.suggest(query, top_k=10)

    return Response({"suggestions": suggestions_list})