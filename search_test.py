import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search = DuckDuckGoSearchRun()

def get_solutions_from_web(problem, university, location):
    print(f"\n🗣️ Student asked: '{problem}'")
    
    # ---  The Translator ---
    print("🧠 Gemini is translating the problem into a smart search query...")
    query_prompt = f"""
    You are an expert at writing search engine queries. 
    Convert this student's problem into a short, 3-to-5 word keyword search query.
    Problem: "{problem}" at {university} in {location} website used for serach will be reddit.
    ONLY reply with the search keywords, absolutely nothing else. No quotes, no intro.
    """
    smart_query = llm.invoke(query_prompt).content.strip()
    
    print(f"🔍 DuckDuckGo is now searching for exactly: '{smart_query}'")
    
    #  search using the SMART query instead of the messy user sentence
    search_results = search.run(smart_query)
    
   
    print("-------------------------------------------\n")
    
    # --- The Summarizer ---
    print("🧠 Gemini is reading the new results and thinking of 3 solutions...")
    prompt = f"""
    You are a helpful student-life assistant for {university}.
    A student has this problem: "{problem}"
    
    Here is raw data scraped from the internet regarding this issue:
    {search_results}
    
    Task: Extract or infer 3 distinct, specific, and actionable solutions or specific places the student can go. 
    If the scraped data is still vague, use your own general knowledge about {university} and {location} to provide REAL store names (like Walmart, Hy-Vee, Fareway, etc.). 
    DO NOT give generic advice. Give me actual names and solutions.
    
    Format them clearly as Option 1, Option 2, Option 3. Keep them concise.
    """
    
    response = llm.invoke(prompt)
    return response.content

# --- TEST AREA ---
if __name__ == "__main__":
    my_university = "University of California"
    my_problem = "where to get cheap groceries near campus"
    my_location = "Los Angeles, CA"
    
    options = get_solutions_from_web(my_problem, my_university, my_location)
    
    print("\n=== THE FINAL RESULTS ===")
    print(options)