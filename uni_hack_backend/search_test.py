import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
import time
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
load_dotenv()
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-lite"
]
search = DuckDuckGoSearchRun()

def execute_with_fallback(prompt):
    """
    Tries to execute a prompt using the available models in sequence.
    If a model hits a rate limit, it falls back to the next one.
    If all models are exhausted, returns "ERROR:RATE_LIMIT".
    """
    for model_name in FALLBACK_MODELS:
        try:
            # Dynamically instantiate the model to catch errors on execution
            llm = ChatGoogleGenerativeAI(model=model_name)
            response = llm.invoke(prompt)
            return response.content
        except ChatGoogleGenerativeAIError as e:
            # Check if the error is due to rate limits/quota exhaustion
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                # Print a warning or log to track that it's falling back
                # print(f"⚠️ {model_name} rate limited. Trying next model...")
                continue  
            raise e  # If it's a different error (e.g., API key issue), raise it immediately
            
    # If the loop finishes without returning, all models failed due to rate limits
    return "ERROR:RATE_LIMIT"

def get_solutions_from_web(problem, university, location, rejected_answers=None):
    if rejected_answers is None:
        rejected_answers = []

    # ---  The Translator ---
    query_prompt = f"""
    You are an expert at writing search engine queries. 
    Convert this student's problem into a short, 3-to-5 word keyword search query.
    Problem: "{problem}" at {university} in {location} website used for search will be reddit.
    ONLY reply with the search keywords, absolutely nothing else. No quotes, no intro.
    """
    time.sleep(3)  # Simulate delay
    
    smart_query = execute_with_fallback(query_prompt)
    
    # If the first step completely exhausts all fallback models, exit early
    if smart_query == "ERROR:RATE_LIMIT":
        return "ERROR:RATE_LIMIT"
        
    smart_query = smart_query.strip()
    
    # Search using the SMART query
    search_results = search.run(smart_query)
    
    # --- The Summarizer ---
    time.sleep(3)  # Simulate delay
    prompt = f"""
    You are a helpful student-life assistant for {university}.

    A student has this problem:
    "{problem}"

    Here is raw data scraped from the internet regarding this issue:
    {search_results}

    Your task:

    * Provide EXACTLY 3 solutions.
    * Each solution must be specific, actionable, and realistic.
    * Prefer REAL place names, businesses, offices, stores, or campus resources whenever possible.
    * If the scraped data is vague, use your own knowledge about {university} and {location} to infer likely real options.
    * DO NOT give generic advice.
    * Keep each option concise (1-3 sentences maximum).

    Negative instructions:

    * Do NOT use markdown formatting.
    * Do NOT use *, #, -, bullet points, or numbered lists except "Option 1", "Option 2", and "Option 3".
    * Do NOT add introductions or conclusions.
    * Do NOT use emojis.
    * Do NOT use quotation marks unless necessary.
    * Do NOT output anything outside the required format.

    Required Output Format:

    Option 1:
    Solution: <specific place/resource/store>
    Why it helps: <short explanation>
    Location/Access: <short location or access detail>

    Option 2:
    Solution: <specific place/resource/store>
    Why it helps: <short explanation>
    Location/Access: <short location or access detail>

    Option 3:
    Solution: <specific place/resource/store>
    Why it helps: <short explanation>
    Location/Access: <short location or access detail>
    IMPORTANT: The student has already rejected the following answers. DO NOT suggest these again:{rejected_answers}.If rejected_answers is empty, ignore that last sentence and provide your best answer based on the search results and your knowledge. If you cannot find any good solutions from the search results, use your knowledge about {university} and {location} to infer likely helpful resources or places.

    Provide a completely new and different solution.
    """
    
    # Execute the final prompt with the fallback system
    final_response = execute_with_fallback(prompt)
    return final_response

# --- TEST AREA ---
'''if __name__ == "__main__":
    my_university = "University of California"
    my_problem = "where to get cheap groceries near campus"
    my_location = "Los Angeles, CA"
    
    options = get_solutions_from_web(my_problem, my_university, my_location)
    
    print("\n=== THE FINAL RESULTS ===")
    print(options)'''