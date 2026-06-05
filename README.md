# Fuzik - Video Upload Prototype

A prototype web application for seamlessly uploading and managing video content, integrated directly with the YouTube Data API.

## Live Demo
- **Frontend (Nuxt):** [[https://fuzik-nuxt4.vercel.app](https://fuzik-nuxt4.vercel.app/)]
- **Backend API (Django):** [https://downloadlovedy.pythonanywhere.com/api/videos/](https://downloadlovedy.pythonanywhere.com/api/videos/)

## Tech Stack
**Frontend:**
- Framework: Nuxt 4 / Vue.js
- Deployment: Vercel

**Backend:**
- Framework: Django & Django REST Framework (DRF)
- Database: SQLite (Hosted on PythonAnywhere with persistent storage)
- Integration: Google OAuth 2.0 & YouTube Data API v3

## Features
- Upload videos directly to a connected YouTube channel via Server-to-Server API.
- Retrieve and display a list of uploaded videos.
- Cross-Origin Resource Sharing (CORS) configured for secure Frontend-Backend communication.

## Local Development Setup

### Backend (Django)
```bash
cd fuzik_backend
python -m venv myvenv
source myvenv/bin/activate  # Or `myvenv\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### Frontend (Nuxt)
```bash
cd fuzik_frontend
npm install
npm run dev
```
Note: client_secrets.json and token.json are required in the backend root directory for YouTube API authentication. They are excluded from this repository for security reasons.
