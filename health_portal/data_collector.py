# File: health_portal/query_suggester.py
import requests
import urllib.parse

# ------------------ Caches ------------------
_openfda_cache = {}  # {query: [reactions]}

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
