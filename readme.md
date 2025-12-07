
# 🏥 Smart Health Backend (Django + DRF)

This is the backend API service for Smart Health Portal, built using Django REST Framework.
It provides semantic health query suggestions and AI-style medical information response generation.

## 🛠 Tech Stack

Technology Use:
Django
Django REST Framework
Suggestify
Spacy
wikiiapi
Python Core language
CORS Headers

## 🔧 Local Setup

```bash

1️⃣ Clone the repo
git clone https://github.com/YOUR_USERNAME/smart_health_backend.git
cd smart_health_backend

2️⃣ Create & activate virtual env
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start server
python manage.py runserver
```

## 🌐 API Endpoints

Method  Endpoint    Description

```bash

GET    /api/suggestions/?q=symptom    Returns related query suggestions
GET /api/health-info/?q=headache Returns detailed health explanation

```

```bash

Example Response — /api/suggestions/
{
  "suggestions": [
    "fever treatment",
    "fever symptoms",
    "how to treat fever"
  ]
}

Example Response — /api/health-info/
{
  "query": "fever",
  "condition": "Fever",
  "causes": ["Infection", "Flu", "Virus"],
  "treatments": ["Rest", "Hydration", "Paracetamol"]
}
```

```bash
🧪 Quick Test
curl http://127.0.0.1:8000/api/suggestions/?q=fever
curl http://127.0.0.1:8000/api/health-info/?q=fever

```

📝 License

Open Source — Feel free to use, improve, and contribute.
