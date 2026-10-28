# 🧹 CleanTrack AI

**CleanTrack AI** is an intelligent, agentic waste-tracking and environmental management platform powered by **FastAPI**, **Google Gemini 2.5 Flash**, **LangChain**, and **LangGraph**. It automatically processes, analyzes, and categorizes community waste reports, extracting critical metadata (severity, authenticity scores, location coordinates, and waste classification) to streamline city cleanup efforts.

---

---

Live demo Link:https://drive.google.com/file/d/1qlCpWtFvEVKLcyrxhbh6gS9E1jUdBzRB/view?usp=sharing
GitHub Repositery Link:https://github.com/rohankadam2007/CleanTrack_AI

---


## 🌟 Key Features

- 🤖 **Agentic Reasoning with LangChain & LangGraph**: Utilizes a **ReAct (Reasoning + Acting) Agent** architecture to process unstructured field reports, make dynamic tool calls, and structure data accurately.
- ⚡ **Powered by Gemini 2.5 Flash**: Leverages Google's high-speed `gemini-2.5-flash` model for intelligent text processing, summary generation, and authenticity evaluation.
- 🚀 **FastAPI Backend**: Light, high-performance async REST API providing endpoints for submitting, processing, and retrieving waste reports.
- 📍 **Geospatial & Contextual Insights**: Tracks latitude, longitude, near-drain risks, and specific waste classifications to prioritize critical cleanup zones.
- 📊 **SQLite Persistence**: Stores complete audit logs and structured reports for city officials, environmental groups, and field workers.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI / Uvicorn
- **AI / Agentic Stack:** Google Gemini API (`google-genai`), LangChain, LangGraph (`langgraph.prebuilt`)
- **Database:** SQLite3
- **Frontend / Static Assets:** HTML5, CSS3, JavaScript (hosted via FastAPI Static Files)

---

## 📁 Project Structure

```
CleanTrack_AI/
├── static/
│   └── index.html          # Frontend web UI / Dashboard
├── venv/                   # Virtual environment (ignored by Git)
├── .env                    # Environment variables (API Keys)
├── .gitignore              # Git ignore file
├── cleantrack.db           # SQLite database for reports
├── main.py                 # FastAPI server & LangChain Agent workflow
├── README.md               # Project documentation
└── requirements.txt        # Project Python dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ installed
- A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

### 2. Clone the Repository
```bash
git clone https://github.com/rohankadam2007/CleanTrack_AI.git
cd CleanTrack_AI
```

### 3. Set Up Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

### 6. Run the Application
```bash
uvicorn main:app --reload
```
Open your browser and navigate to `http://127.0.0.1:8000` to view the application or `http://127.0.0.1:8000/docs` to interact with the API documentation.

---

## 🌐 Deployment

### Deploying to Render
1. Push your latest code to GitHub.
2. Sign in to [Render](https://render.com/) and create a new **Web Service**.
3. Connect your repository (`rohankadam2007/CleanTrack_AI`).
4. Set the build configuration:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Under **Environment Variables**, add `GEMINI_API_KEY`.
6. Click **Deploy**!

---

## 👥 Contributors

- **Rohan Kadam** ([@rohankadam2007](https://github.com/rohankadam2007)) 
- Dhanushree A
- chandana KR
- 

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).


\
