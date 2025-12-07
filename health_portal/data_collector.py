# File: health_portal/query_suggester.py
import requests
import urllib.parse

# ------------------ Caches ------------------
_medline_cache = {}  # {query: [topics]}
_openfda_cache = {}  # {query: [reactions]}

# ------------------ MedlinePlus ------------------
def fetch_medlineplus_topics(query):
    """Fetch MedlinePlus topics dynamically with caching."""
    if query in _medline_cache:
        return _medline_cache[query]

    url = "https://wsearch.nlm.nih.gov/ws/query"
    encoded_query = urllib.parse.quote(query)
    params = {
        "db": "healthTopics",
        "term": encoded_query,
        "max": 20,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            topics = [item.get("title", "") for item in data.get("records", [])]
            _medline_cache[query] = topics
            return topics
        else:
            print("❗MedlinePlus HTTP error:", response.status_code)
    except Exception as e:
        print("❗MedlinePlus fetch exception:", e)

    return []

# ------------------ OpenFDA ------------------
def fetch_openfda_matches(query):
    """Fetch OpenFDA drug reactions dynamically with caching."""
    if query in _openfda_cache:
        return _openfda_cache[query]

    try:
        response = requests.get(
            "https://api.fda.gov/drug/event.json",
            params={"search": f"patient.reaction.reactionmeddrapt:{query}", "limit": 50},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            reactions = [
                item.get("patient", {})
                    .get("reaction", [{}])[0]
                    .get("reactionmeddrapt", "")
                for item in data.get("results", [])
            ]
            _openfda_cache[query] = reactions
            return reactions
    except Exception as e:
        print("❗OpenFDA fetch exception:", e)

    return []
