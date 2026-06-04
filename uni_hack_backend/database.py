import os
import uuid
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in environment variables. Please add it to your .env file.")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("university-knowledge")

# 2. Initialize a local embedding model (Outputs 384-dimensional vectors to match your old Chroma setup)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Kept exactly at 0.35 to preserve your precision configuration
MATCH_THRESHOLD = 0.35

def normalize(text: str) -> str:
    """Normalizes text: lowercases, strips, and collapses all whitespace."""
    return " ".join(text.lower().split())

def save_to_library(problem_topic, solution_text, author_name, status, university, location):
    """Saves ANY solution into the permanent cloud Pinecone database."""
    entry_id = str(uuid.uuid4())

    # Generate the math vector array for the problem topic
    vector = model.encode(problem_topic).tolist()

    # Pinecone inserts documents as a tuple: (ID, Vector, Metadata)
    index.upsert(
        vectors=[
            (
                entry_id, 
                vector, 
                {
                    "problem": problem_topic, 
                    "solution": solution_text,
                    "author":   author_name,
                    "status":   status,
                    "university": normalize(university),
                    "location":   normalize(location)
                }
            )
        ]
    )
    print(f"Successfully saved hack {entry_id} to Pinecone Cloud!")

def search_library(query_topic, university, location):
    """Searches the cloud database for the closest matching solutions using Metadata filtering."""
    
    # Convert incoming search string into a matching 384-dim vector
    query_vector = model.encode(query_topic).tolist()

    # Query the Pinecone Index
    response = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True,
        filter={
            "university": {"$eq": normalize(university)},
            "location": {"$eq": normalize(location)}
        }
    )

    # RECONSTRUCT DATA: Format the dictionary to look exactly like ChromaDB's output
    db_results = {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    for match in response.get('matches', []):
        # Convert Pinecone's Similarity Score into Cosine Distance
        distance = 1.0 - match['score']
        
        db_results["documents"][0].append(match['metadata']['problem'])
        db_results["metadatas"][0].append(match['metadata'])
        db_results["distances"][0].append(distance)

    return db_results

'''def wipe_database():
    """Deletes all vectors within the index namespace to start fresh."""
    print("Wiping the cloud database clean...")
    try:
        index.delete(delete_all=True)
        print("Cloud database is now completely empty!")
    except Exception as e:
        print(f"Index is already empty or wipe failed: {e}")

if __name__ == "__main__":
    pass'''