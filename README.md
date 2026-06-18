# UniHack — Student Knowledge Base

> Real hacks from real students. AI when you need it.
> **Live Demo:** https://unihack-frontend.onrender.com/

UniHack is a community-powered search tool that helps university students find solutions to campus problems. It first searches a crowd-sourced database of student-submitted hacks, and falls back to AI-powered web search when nothing is found locally.

---

## Why UniHack?

Students often spend hours searching Reddit, Discord servers, Facebook groups, and university websites trying to solve problems that other students have already solved before. UniHack makes that knowledge searchable and reusable.

Not every useful piece of knowledge is written in an official guide. Many solutions exist only through word of mouth:

- Where can I buy groceries cheaply near campus?
- What's the cheapest way to get a ride home?
- Which dining hall has the best food?
- How do I fix the university Wi-Fi issue?
- Where are the quietest study spots?
- Which professor's office hours are actually helpful?

When a student submits a solution, it becomes part of a searchable knowledge base for future students at the same university and location. If a problem has never been solved before, UniHack automatically uses Google Gemini and web search to find the best possible answer — and when that solution helps someone, it gets saved so future students benefit too.

The result is a continuously growing knowledge base where every solved problem makes life easier for the next student.

---

## Features

- 🔍 Semantic search using vector embeddings
- 🎓 University-specific knowledge filtering
- 📍 Location-aware results
- 🤝 Community-submitted student solutions
- 🤖 AI-powered fallback search using Gemini
- 🌐 Web-assisted search via DuckDuckGo
- 👍 Feedback system for result quality
- 🚫 Automatic blocking of incorrect matches after 3 reports
- ⚡ FastAPI backend with Vanilla JavaScript frontend

---

## Table of Contents

- [Why UniHack?](#why-unihack)
- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [API Reference](#api-reference)
- [Database & Embedding](#database--embedding)
- [Feedback & Block System](#feedback--block-system)
- [Frontend Guide](#frontend-guide)
- [Running Locally (No Server)](#running-locally-no-server)
- [Deployment](#deployment)
- [License](#license)

---

## How It Works

```
User enters a problem + university + location
            ↓
Search Pinecone vector database
(filtered by university + location)
            ↓
Match found (distance < 0.35)?
    YES → Return DB result + ask "Was this relevant?"
            ↓ No → Why?
                Option 1: Different solution → search again
                Option 2: Different problem  → record block, search again
    NO  → Fall back to AI web search (Gemini + DuckDuckGo)
            ↓
AI result shown → ask "Did this work?"
    YES → Save to database for future students
    NO  → Try again (max 3 attempts)
```

---

## Project Structure

```
unihack-bot/
│
├── uni_hack_backend/
│   ├── server.py           # FastAPI backend — all HTTP endpoints
│   ├── database.py         # Pinecone vector DB + SQLite feedback block system
│   ├── search_test.py      # AI web search using Gemini + DuckDuckGo
│   ├── main.py             # CLI version of the app (for local testing)
│   ├── test.py             # Integration test runner
│   ├── requirements.txt    # Python dependencies
│   └── feedback_blocks.db  # Auto-generated SQLite file (do not edit manually)
│
├── uni_hack_frontend/
│   ├── index.html          # Main search page
│   ├── submit.html         # Student hack submission page
│   ├── app.js              # Frontend logic for search + feedback
│   ├── submit.js           # Frontend logic for submission form
│   └── style.css           # Shared stylesheet (cyberpunk theme)
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Tech Stack

| Layer             | Technology                                                             |
| ----------------- | ---------------------------------------------------------------------- |
| Frontend          | Vanilla HTML, CSS, JavaScript                                          |
| Backend           | Python, FastAPI                                                        |
| Vector Database   | Pinecone (cloud)                                                       |
| Embeddings        | `sentence-transformers/all-MiniLM-L6-v2` via FastEmbed (runs locally) |
| AI Web Search     | Google Gemini (via LangChain) + DuckDuckGo                             |
| Feedback Storage  | SQLite (local file)                                                    |
| Hosting (backend) | Render                                                                 |

---

## Setup & Installation

### Prerequisites

- Python 3.9+
- A Pinecone account with an index named `university-knowledge`
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/Sam00-B/unihack-bot.git
cd unihack-bot
```

### 2. Install Python dependencies

```bash
cd uni_hack_backend
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file inside `uni_hack_backend/`:

```
PINECONE_API_KEY=your_pinecone_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

### 4. Create your Pinecone index

In your Pinecone dashboard, create an index with:

- **Name:** `university-knowledge`
- **Dimensions:** `384` (matches `all-MiniLM-L6-v2`)
- **Metric:** `cosine`

---

## Environment Variables

| Variable           | Required | Description                 |
| ------------------ | -------- | --------------------------- |
| `PINECONE_API_KEY` | Yes      | Your Pinecone cloud API key |
| `GOOGLE_API_KEY`   | Yes      | Your Google Gemini API key  |

---

## Running the App

### Start the backend server

From inside `uni_hack_backend/`:

```bash
uvicorn server:app --reload
```

Server runs at `http://127.0.0.1:8000`

### Open the frontend

Open `uni_hack_frontend/index.html` directly in your browser, or serve it with any static file server:

```bash
npx serve uni_hack_frontend/
```

### Switch between local and production backend

At the top of both `uni_hack_frontend/app.js` and `uni_hack_frontend/submit.js`:

```js
const BACKEND_URL = "https://unihack-bot.onrender.com"; // production
// const BACKEND_URL = "http://127.0.0.1:8000";          // local dev
```

Comment/uncomment as needed.

---

## API Reference

### `POST /ask`

Search for a solution to a campus problem.

**Request body:**

```json
{
  "problem": "wifi not connecting in dorm",
  "university": "University of South Dakota",
  "location": "Vermillion, SD",
  "rejected_answers": []
}
```

**Response (database hit):**

```json
{
  "type": "hybrid_solution",
  "solution": "Official or AI-verified answer (or null)",
  "hacks": [
    { "author": "Student Name", "solution": "Their tip here" }
  ],
  "source": "db"
}
```

**Response (web search):**

```json
{
  "type": "ai_solution",
  "solution": "Option 1:\nSolution: ...\nWhy it helps: ...",
  "source": "web"
}
```

**Response (exhausted / error):**

```json
{
  "type": "ai_solution",
  "solution": "Sorry, we couldn't find...",
  "source": "exhausted"
}
```

---

### `POST /submit`

Submit a student hack to the database.

**Request body:**

```json
{
  "problem": "free parking near campus",
  "university": "University of South Dakota",
  "location": "Vermillion, SD",
  "solution": "Park on Pine Street after 6pm, it's free.",
  "author": "Alex"
}
```

**Response:**

```json
{ "status": "success", "message": "Hack saved successfully!" }
```

---

### `POST /save_answer`

Called automatically when a user clicks "Yes" on a web search result. Saves the AI answer to the database as a verified solution for future students.

**Request body:**

```json
{
  "problem": "wifi not connecting",
  "university": "University of South Dakota",
  "location": "Vermillion, SD",
  "solution": "The AI-generated answer text"
}
```

---

### `POST /report_feedback`

Called when a user clicks "No → Answer to a different problem" on a database result. Records the bad query→result pair. After 3 reports from different users, that pair is permanently blocked.

**Request body:**

```json
{
  "query": "wifi not connecting",
  "result_problem": "wifi keeps disconnecting",
  "university": "University of South Dakota",
  "location": "Vermillion, SD",
  "reason": "different_problem"
}
```

`reason` values:

- `different_problem` — wrong match entirely; counts toward the block threshold
- `different_solution` — right topic, wrong fix; soft signal only, never blocks

---

### `GET /`

Health check.

```json
{ "message": "UniHack API is live and running! 🚀" }
```

---

## Database & Embedding

### How vectors are stored

Every problem submitted to the database is converted into a 384-dimensional vector using `sentence-transformers/all-MiniLM-L6-v2` running locally via FastEmbed. This vector captures the semantic meaning of the text.

```python
vector = list(model.embed([problem_topic]))[0].tolist()
```

### How search works

A query is embedded the same way, then Pinecone finds the closest stored vectors using cosine similarity. Results are filtered strictly by `university` and `location` — data from other universities is completely invisible.

### Distance vs similarity

Pinecone returns a similarity score (0–1, higher = better match). The code converts it to a distance (lower = better) for threshold comparison:

```python
distance = 1.0 - match['score']
```

### Match threshold

```python
MATCH_THRESHOLD = 0.35
```

Results with `distance > 0.35` (similarity < 0.65) are discarded as too weak a match.

### Solution status types

| Status         | Set by                            | Shown as               |
| -------------- | --------------------------------- | ---------------------- |
| `pending`      | Student submissions via `/submit` | "Student Tip" card     |
| `verified`     | User clicks "Yes" on a web result | Official solution card |
| `ai_generated` | Reserved for future use           | Official solution card |

---

## Feedback & Block System

The feedback block system prevents the vector database from repeatedly returning semantically similar but contextually wrong answers (e.g., returning "wifi disconnecting" when the user asked about "wifi not connecting").

### Storage

Blocks are stored in a local SQLite file (`feedback_blocks.db`) with two tables:

**`feedback_reports`** — one row per user per reported pair:

```
query | blocked_result | university | location | user_id | reason
```

**`block_list`** — running count per unique pair:

```
query | blocked_result | university | location | report_count
```

### Block threshold

```python
BLOCK_THRESHOLD = 3
```

A query→result pair is blocked for everyone at that university+location only after **3 different users** report it as "a different problem." This prevents one bad report from ruining results for everyone.

### How blocks are applied

In `search_library()`, after Pinecone returns results, each result is checked against the block list before being included:

```python
if _is_blocked(query_topic, result_problem, university, location):
    continue  # skip this result silently
```

The search fetches `top_k=10` from Pinecone internally, filters blocked results, and returns at most 3 clean results — same output as before, just with bad matches removed.

---

## Frontend Guide

### Pages

- `uni_hack_frontend/index.html` — search page
- `uni_hack_frontend/submit.html` — submission form

### Result card types

| CSS class       | Border color | Used for                |
| --------------- | ------------ | ----------------------- |
| `.ai-card`      | Purple       | AI/verified solutions   |
| `.student-card` | Green        | Student-submitted hacks |

### Feedback flow (app.js)

```
DB result   → "Was this relevant to your problem?" Yes / No
Web result  → "Did this solution work for you?"    Yes / No
                                                        ↓ No
                                               "Why wasn't it helpful?"
                                               [1. The solution is different]
                                               [2. Answer to a different problem]
```

- **Option 1** from DB → soft signal, searches again, no block recorded
- **Option 2** from DB → reports to `/report_feedback`, searches again
- **Yes** on web result → saves to database via `/save_answer`
- **Yes** on DB result → no save (already in database)

### Location input hint

Users are guided on how to format the location field:

- USA/Canada: `City, State` (e.g. Austin, Texas)
- Other countries: `City, Country` (e.g. London, UK)

This matters because location is used as a strict equality filter in Pinecone — inconsistent formatting would cause misses.

---

## AI Model Fallback Chain

The web search uses Google Gemini with automatic fallback if rate limits are hit:

```
gemini-2.5-flash → gemini-2.5-flash-lite → gemini-1.5-flash → gemini-1.5-flash-lite
```

If all models are exhausted, the API returns `source: "error"` and no feedback buttons are shown.

---

## Running Locally (No Server)

If you want to run UniHack entirely on your own machine without deploying anything, follow these steps. Everything works locally — the only external services used are Pinecone (cloud) and Google Gemini (API call).

### Step 1 — Complete setup first

Make sure you have done the full [Setup & Installation](#setup--installation) steps: dependencies installed, `.env` file created, and Pinecone index created.

### Step 2 — Start the backend locally

From inside `uni_hack_backend/`:

```bash
uvicorn server:app --reload
```

This starts the API at `http://127.0.0.1:8000`. Keep this terminal open while using the app.

### Step 3 — Switch the frontend to local mode

In both `uni_hack_frontend/app.js` and `uni_hack_frontend/submit.js`, comment out the production URL and uncomment the local one:

```js
// const BACKEND_URL = "https://unihack-bot.onrender.com";
const BACKEND_URL = "http://127.0.0.1:8000"; // ← use this for local
```

### Step 4 — Open the frontend

Open `uni_hack_frontend/index.html` directly in your browser. No extra server needed — just double-click the file or drag it into your browser.

Or use a simple static server if you prefer:

```bash
# Python (built-in)
python -m http.server 3000 --directory uni_hack_frontend/
# Then open http://localhost:3000
```

### Step 5 — Verify everything is working

Open your browser and go to:

```
http://127.0.0.1:8000/
```

You should see:

```json
{ "message": "UniHack API is live and running! 🚀" }
```

If you see this, the backend is running correctly and the frontend will work.

---

### Using the CLI version locally (no browser needed)

If you want to test without a browser at all, `main.py` is a fully working command-line version of the app:

```bash
python uni_hack_backend/main.py
```

By default it runs a test query at the bottom of `main.py`:

```python
if __name__ == "__main__":
    ask_unihack("eduroam wifi is not connecting", "University of South Dakota", "Vermillion, SD")
```

Change that line to test any problem, university, and location you want. The CLI version prompts you directly in the terminal for yes/no feedback and lets you type your own solution if nothing is found.

---

### Common local issues

| Problem                        | Fix                                                                        |
| ------------------------------ | -------------------------------------------------------------------------- |
| `PINECONE_API_KEY not found`   | Make sure `.env` is inside `uni_hack_backend/` and `python-dotenv` is installed |
| `Connection Error` in browser  | Backend is not running — start it with `uvicorn server:app --reload`       |
| CORS error in browser          | You're pointing at the wrong `BACKEND_URL` — check `app.js`                |
| `ModuleNotFoundError`          | Run `pip install -r requirements.txt` inside `uni_hack_backend/`           |
| Pinecone returns no results    | Your index may be empty — submit a hack first via `submit.html`            |
| `feedback_blocks.db` not found | It is created automatically on first run — no action needed                |

---

## Deployment

### Backend (Render)

1. Push your code to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Set the **Root Directory** to `uni_hack_backend`
4. Set the start command: `uvicorn server:app --host 0.0.0.0 --port 10000`
5. Add environment variables: `PINECONE_API_KEY`, `GOOGLE_API_KEY`
6. Copy your Render URL into `uni_hack_frontend/app.js` and `uni_hack_frontend/submit.js` as `BACKEND_URL`

### Frontend

The frontend is plain HTML/CSS/JS — host the `uni_hack_frontend/` folder anywhere:

- GitHub Pages
- Netlify (drag and drop the folder)
- Vercel

### Note on SQLite in production

`feedback_blocks.db` is a local file. On Render's free tier, the filesystem resets on each deploy, so feedback block data does not persist between deploys. This is a known limitation.
---

## License

This project is open-source and available under the [MIT License](LICENSE).
