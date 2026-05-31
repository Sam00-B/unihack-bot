from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database
import search_test

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    problem: str
    university: str
    location: str
    rejected_answers: list = []  # NEW: Tracks bad answers

class SubmitRequest(BaseModel):
    problem: str
    university: str
    location: str
    solution: str
    author: str

class SaveAnswerRequest(BaseModel): # NEW: Used when a student clicks "Yes"
    problem: str
    university: str
    location: str
    solution: str

@app.post("/ask")
def ask_unihack_api(req: QueryRequest):
    print(f"Incoming search: '{req.problem}'. Rejected count: {len(req.rejected_answers)}")
    
    # 1. ONLY search the database if this is our first try (no rejected answers yet)
    if not req.rejected_answers:
        db_results = database.search_library(req.problem, req.university, req.location)
        
        if not db_results['documents'] or not db_results['documents'][0]:
            documents, metadatas, distances = [], [], []
        else:
            documents = db_results['documents'][0]
            metadatas = db_results['metadatas'][0]
            distances = db_results['distances'][0]
            
        main_answer = None
        pending_hacks = []
     
        for i in range(len(documents)):
            if distances[i] < 0.4:
                status = metadatas[i]['status']
                author = metadatas[i]['author']
                solution_text = metadatas[i]['solution']
                
                if status in ['ai_generated', 'verified'] and main_answer is None:
                    main_answer = solution_text
                elif status == 'pending':
                    if {"author": author, "solution": solution_text} not in pending_hacks:
                        pending_hacks.append({"author": author, "solution": solution_text})
        
        if pending_hacks:
            return {"type": "student_hacks", "hacks": pending_hacks, "source": "db"}
            
        if main_answer:
            return {"type": "ai_solution", "solution": main_answer, "source": "db"}
            
    # 2. Stop trying if we hit 3 rejected answers
    if len(req.rejected_answers) >= 3:
        return {
            "type": "ai_solution", 
            "solution": "Sorry, we couldn't find a good solution from the web after 3 tries. If you figure it out yourself, please use the 'Submit a Hack' button to help future students!", 
            "source": "exhausted"
        }

    # 3. Search the web, passing in the bad answers to avoid them
    print("Searching the web...")
    web_answer = search_test.get_solutions_from_web(req.problem, req.university, req.location, req.rejected_answers)
    
    if web_answer == "ERROR:RATE_LIMIT":
        return {"type": "ai_solution", "solution": "🛑 Out of Juice! UniHack has hit its AI token limit for the moment. Please check back in a little while!", "source": "error"}
    
    # Notice we DO NOT save to the database here! We wait for the user to click Yes.
    return {"type": "ai_solution", "solution": web_answer, "source": "web"}


@app.post("/save_answer")
def save_answer_api(req: SaveAnswerRequest):
    # This triggers when the user clicks "Yes"
    print("User clicked Yes! Saving verified answer to database...")
    database.save_to_library(req.problem, req.solution, "UniHack AI", "verified", req.university, req.location)
    return {"status": "success"}


@app.post("/submit")
def submit_hack_api(req: SubmitRequest):
    print(f"New hack submitted by {req.author} for {req.problem}")
    try:
        database.save_to_library(req.problem, req.solution, req.author, "pending", req.university, req.location)
        return {"status": "success", "message": "Hack saved successfully!"}
    except Exception as e:
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save to database.")