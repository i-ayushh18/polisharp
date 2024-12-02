# Polisharp

PoliSharp is an AI-powered tool that simplifies complex privacy policies. By providing a URL or uploading a PDF of a privacy policy, users receive a concise, tabular summary, enabling them to understand critical information quickly and easily.

## 🚀 Features
- **URL & PDF Input**: Accepts privacy policies via URL or file upload.
- **AI-Powered Summarization**: Processes lengthy and dense policies using advanced AI algorithms.
- **Tabular Output**: Presents key points (e.g., data collection, purpose, and criticality) in a user-friendly table.
- **Enhanced Transparency**: Helps users make informed decisions regarding their data privacy.

## 🛠️ Tech Stack
- **Frontend**: SvelteKit with TailwindCSS for a modern, responsive user interface.
- **Backend**: Python (FastAPI) for processing and AI integration.
- **AI Integration**: Utilizes Google Gemini's large language models (LLMs) for natural language processing.

## 📦 Installation
- Clone the repository:
```bash
git clone https://github.com/your-username/polisharp.git
cd polisharp
```
- Set up the backend:
```
cd backend
python3 -m venv venv
source venv/bin/activate # for bash
# OR
venv/scripts/activate # for powershell
pip install -r requirements.txt
```
- Setup Gemini API Key (Critical: One must be satisfied)
    - Create a new file with the name `.env` in backend dir.
    - Paste the following `GEMINI_API_KEY=<your_api_key>`.
OR
    - Put the api key in the Gemini API Key field.
- Set up the frontend:
```bash
cd ../frontend
npm install
```
## 🚀 Usage
- Start the backend (available at `https://localhost:8000`):
```bash
cd backend
uvicorn main:app
```
- Start the frontend:
```bash
cd frontend
npm run dev
```
Access the app in your browser at http://localhost:5173.

## 📜 License
This project is licensed under the [MIT License](./LICENSE).