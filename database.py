import chromadb
import uuid

# Initialize the Database
client = chromadb.PersistentClient(path="./local_db")
collection = client.get_or_create_collection(name="university_knowledge")

def save_to_library(problem_topic, solution_text, author_name, status):
    """Saves ANY solution (AI or Student) into the local database with metadata tags."""
    
    entry_id = str(uuid.uuid4())
    #print(f"💾 Saving solution to library (Author: {author_name} | Status: {status})...")
    
    collection.add(
        documents=[solution_text],
        metadatas=[{
            "topic": problem_topic, 
            "author": author_name, 
            "status": status
        }],
        ids=[entry_id]
    )
    #print("✅ Saved successfully!\n")

def search_library(query_topic):
    """Searches the database for the closest matching solutions."""
    
    #print(f"🔍 Searching local library for: '{query_topic}'...")
    
    # Return the top 3 closest matches this time so we can see multiple types
    results = collection.query(
        query_texts=[query_topic],
        n_results=3  
    )
    
    return results
def wipe_database():
    """Deletes the entire collection to start fresh."""
    print("🧨 Wiping the database clean...")
    client.delete_collection(name="university_knowledge")
    print("✅ Database is now completely empty!")

# --- TEST AREA ---
"""":
    print("=== 1. SAVING AN AI-GENERATED WEB SOLUTION ===")
    save_to_library(
        problem_topic="where to get cheap groceries near campus",
        solution_text="Option 1: Walmart on Broadway. Option 2: Hy-Vee on Main. Option 3: Fareway.",
        author_name="UniHack AI",
        status="ai_generated"
    )

   
    
    print("=== 3. NEW STUDENT ASKS THE QUESTION ===")
    search_results = search_library("cheap food options")
    
    print("\n--- RAW DATABASE RESULTS ---")
    print(search_results['metadatas']) # Just printing the metadata so it's easier to read
    print("----------------------------\n")"""
if __name__ == "__main__":
    print("=== 2. SAVING A STUDENT HACK ===")
    save_to_library(
        problem_topic="where to get cheap groceries near campus",
        solution_text="you can get cheap groceries from global bazaar",
        author_name="Alex",
        status="pending"
    )


# --- QUICK WIPE SCRIPT ---
"""if __name__ == "__main__":
    # Uncomment the line below, run python database.py, then comment it out again!
    wipe_database()"""