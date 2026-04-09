# PathEdge — AI Career Coach & Mock Interview Coach

> An AI-powered career portal helping college students land their dream jobs. Built for UN SDG Goal 8: Decent Work & Economic Growth.

PathEdge is a full-stack intelligent career assistant. Students can have a natural conversation with the AI to conduct mock interviews (Technical, HR, Resume Review), or receive a personalised **Job Prediction Report** based on their skills and geographic location — all powered by **LangGraph**, **Groq (Llama 3.3)**, **FastAPI**, **Supabase**, and **React + Tailwind CSS**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Intent Router** | Automatically classifies your career need from natural language |
| 🎯 **Technical Mock Interview** | Asks one focused technical question at a time with feedback |
| 👔 **HR Mock Interview** | Practices behavioral questions and communication skills |
| 📝 **Resume Review Coach** | Guides you to strengthen your resume through conversation |
| 📍 **Job Prediction Agent** | Predicts best-fit roles, local companies & skill gaps based on skills + location |
| 📊 **Live Profile Tracker** | Real-time side panel tracking name, role, skills, location & mode |
| 🗄️ **Supabase Logging** | Automatically saves session feedback to the cloud database |

---

## 🛠️ Tech Stack

- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: Python 3.11 + FastAPI + Uvicorn
- **AI Workflow**: LangGraph + LangChain
- **LLM**: Groq (`llama-3.3-70b-versatile`)
- **Database**: Supabase (PostgreSQL)

---

## ⚙️ Setup Guide

### Prerequisites
- Node.js 18+
- Python 3.9+
- A [Groq API Key](https://console.groq.com/) (free)
- A [Supabase](https://supabase.com/) account (free)

---

### 1. Supabase Database Setup

1. Go to [supabase.com](https://supabase.com/) and create a **New Project**.
2. In the left sidebar, open the **SQL Editor**.
3. Paste the contents of `backend/schema.sql` into the editor and click **Run**.
4. Go to **Project Settings → API** and copy:
   - **Project URL**
   - **anon public API Key**

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `.env` with your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here

SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🚀 How to Use

1. **Start a conversation** — Tell PathEdge your name, target role, and location.
2. **Choose your mode** — Say "Technical Interview", "HR Interview", "Resume Review", or "Job Prediction".
3. **Practice** — The AI asks one question at a time and gives feedback before each next question.
4. **Get your Job Report** — If you choose Job Prediction, PathEdge analyses local market demand for your skill set.
5. **End the session** — Type `stop` at any time. Your session feedback is automatically saved to Supabase.

---

## 📁 Project Structure

```
PathEdge/
├── backend/
│   ├── agent.py          # LangGraph AI workflow & all nodes
│   ├── main.py           # FastAPI routes & Supabase logging
│   ├── schema.sql        # Database table definitions
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Environment variable template
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.jsx   # Main chat UI
    │   │   └── StudentCard.jsx     # Live profile tracker sidebar
    │   └── App.jsx                 # Root layout
    ├── public/
    │   └── favicon.svg             # PathEdge logo
    └── index.html
```

---

## 🌍 SDG Alignment

PathEdge directly supports **UN Sustainable Development Goal 8** — *Decent Work and Economic Growth* — by equipping college students with intelligent, personalised career coaching that was previously only accessible through expensive coaching services.

---

## 📄 License

MIT License © 2026 PathEdge
