# UniHack 🎓

> Real student problems. Real student solutions. AI when needed.

UniHack is a community-powered platform that helps university students solve campus-related problems by combining student knowledge, semantic search, and AI-powered web search.

Students often spend hours searching Reddit, Discord servers, Facebook groups, university websites, and random forums trying to solve problems that other students have already solved before. UniHack makes that knowledge searchable and reusable.

---

# Why UniHack?

Not every useful piece of knowledge is written in an official guide.

Many student solutions exist only through word of mouth:

* Where can I buy groceries cheaply near campus?
* What's the cheapest way to get a ride home?
* Which dining hall has the best food?
* How do I fix the university Wi-Fi issue?
* Where are the quietest study spots?
* Which professor's office hours are actually helpful?

Usually students learn these things after spending hours searching online, asking around, or experimenting themselves.

But what if a senior student already faced the exact same problem and found the answer?

UniHack was built to preserve and share those experiences.

When a student submits a solution, it becomes part of a searchable knowledge base for future students at the same university and location.

If a problem has never been solved before, UniHack automatically uses Google Gemini and web search to find the best possible answer. When that AI-generated solution helps the student, it can be saved to the database so future students can benefit from it as well.

The result is a continuously growing knowledge base where every solved problem makes life easier for the next student.

---

# ✨ Features

* 🔍 Semantic search using vector embeddings
* 🎓 University-specific knowledge filtering
* 📍 Location-aware results
* 🤝 Community-submitted student solutions
* 🤖 AI-powered fallback search using Gemini
* 🌐 Web-assisted search using DuckDuckGo
* 👍 Feedback system for result quality
* 🚫 Automatic blocking of incorrect matches
* ⚡ FastAPI backend with Vanilla JavaScript frontend

---

# 🚀 How It Works

```text
Student submits a problem
        ↓
Search UniHack knowledge base
        ↓
Relevant answer found?
     YES                NO
      ↓                  ↓
Return student      AI web search
and verified tips        ↓
      ↓            Generate solution
Collect feedback         ↓
      ↓            Student confirms
Improve search           ↓
                    Save for future use
```

---

# 🏗️ Tech Stack

| Layer           | Technology                   |
| --------------- | ---------------------------- |
| Frontend        | HTML, CSS, JavaScript        |
| Backend         | FastAPI                      |
| Vector Database | Pinecone                     |
| Embeddings      | FastEmbed + all-MiniLM-L6-v2 |
| AI Search       | Google Gemini                |
| Web Search      | DuckDuckGo                   |
| Local Storage   | SQLite                       |
| Hosting         | Render                       |

---

# 📂 Project Structure

```text
unihack/
│
├── index.html
├── submit.html
├── app.js
├── submit.js
├── style.css
│
├── server.py
├── database.py
├── search_test.py
├── main.py
├── test.py
│
├── requirements.txt
└── feedback_blocks.db
```

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/unihack.git
cd unihack
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create Environment Variables

Create a `.env` file:

```env
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

## Create Pinecone Index

Index Name:

```text
university-knowledge
```

Settings:

```text
Dimension: 384
Metric: cosine
```

---

# ▶️ Running the Project

Start the FastAPI backend:

```bash
uvicorn server:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Open `index.html` in your browser or run:

```bash
npx serve .
```

---

# 🔌 API Endpoints

## POST /ask

Search for a solution.

```json
{
  "problem": "wifi not connecting in dorm",
  "university": "University of South Dakota",
  "location": "Vermillion, SD"
}
```

---

## POST /submit

Submit a student solution.

```json
{
  "problem": "free parking near campus",
  "university": "University of South Dakota",
  "location": "Vermillion, SD",
  "solution": "Park on Pine Street after 6 PM.",
  "author": "Alex"
}
```

---

## POST /save_answer

Save an AI-generated answer that successfully solved a student's problem.

---

## POST /report_feedback

Report incorrect search results.

---

## GET /

Health check endpoint.

```json
{
  "message": "UniHack API is live and running!"
}
```

---

# 🧠 Search Architecture

### Step 1 — Semantic Search

Every problem is converted into embeddings using:

```python
sentence-transformers/all-MiniLM-L6-v2
```

The query is compared against previously solved problems stored in Pinecone.

---

### Step 2 — University & Location Filtering

Results are filtered by:

* University
* Location

Students only see solutions relevant to their own campus.

---

### Step 3 — AI Fallback

If no reliable match is found:

```text
Gemini + DuckDuckGo Search
```

generates a new solution.

---

### Step 4 — Learning from Success

If the AI-generated solution works:

```text
Student clicks YES
        ↓
Answer saved to database
        ↓
Future students benefit
```

Every successful solution improves UniHack's knowledge base.

---

# 👍 Feedback System

UniHack continuously improves search quality.

Users can report:

* Wrong solution
* Wrong problem match

Incorrect query-result pairs are tracked and automatically blocked after enough reports from different users.

This prevents the same bad matches from repeatedly appearing.

---

# 🌐 Deployment

## Backend

Deploy on Render:

```bash
uvicorn server:app --host 0.0.0.0 --port 10000
```

Add:

```env
PINECONE_API_KEY
GOOGLE_API_KEY
```

to Render environment variables.

---

## Frontend

Can be hosted on:

* GitHub Pages
* Netlify
* Vercel

---

# 📜 License

This project is open-source and available under the MIT License.
