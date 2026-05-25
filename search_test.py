import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
import time
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search = DuckDuckGoSearchRun()

def get_solutions_from_web(problem, university, location, rejected_answers=[]):
    if rejected_answers is None:
        rejected_answers = []

    #print(f"\n🗣️ Student asked: '{problem}'")
    
    # ---  The Translator ---
    #print("🧠 Gemini is translating the problem into a smart search query...")
    query_prompt = f"""
    You are an expert at writing search engine queries. 
    Convert this student's problem into a short, 3-to-5 word keyword search query.
    Problem: "{problem}" at {university} in {location} website used for serach will be reddit.
    ONLY reply with the search keywords, absolutely nothing else. No quotes, no intro.
    """
    time.sleep(3)  # Simulate delay
    smart_query = llm.invoke(query_prompt).content.strip()
    
    #print(f"🔍 DuckDuckGo is now searching for exactly: '{smart_query}'")
    
    #  search using the SMART query instead of the messy user sentence
    search_results = search.run(smart_query)
    
   
    #print("-------------------------------------------\n")
    
    # --- The Summarizer ---
    #print("🧠 Gemini is reading the new results and thinking of 3 solutions...")
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
                Name: <specific place/resource/store>
                Why it helps: <short explanation>
                Location/Access: <short location or access detail>

                Option 2:
                Name: <specific place/resource/store>
                Why it helps: <short explanation>
                Location/Access: <short location or access detail>

                Option 3:
                Name: <specific place/resource/store>
                Why it helps: <short explanation>
                Location/Access: <short location or access detail>
                IMPORTANT: The student has already rejected the following answers. DO NOT suggest these again:{rejected_answers}.If rejected_answers is empty, ignore that last sentence and provide your best answer based on the search results and your knowledge. If you cannot find any good solutions from the search results, use your knowledge about {university} and {location} to infer likely helpful resources or places.

                Provide a completely new and different solution.

                    """
    
    response = llm.invoke(prompt)
    return response.content

# --- TEST AREA ---
"""if __name__ == "__main__":
    my_university = "University of California"
    my_problem = "where to get cheap groceries near campus"
    my_location = "Los Angeles, CA"
    
    options = get_solutions_from_web(my_problem, my_university, my_location)
    
    print("\n=== THE FINAL RESULTS ===")
    print(options)"""