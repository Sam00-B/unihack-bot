import chromadb
import uuid
from chromadb.utils import embedding_functions

# Initialize the Database
client = chromadb.PersistentClient(path="./local_db")

# Swap the default embedding model for one trained on Q&A / problem matching.
# "multi-qa-mpnet-base-dot-v1" understands that "not connecting" and
# "disconnecting" are different problems, unlike the default all-MiniLM-L6-v2
# which only cares about topic similarity.

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="multi-qa-mpnet-base-dot-v1"
)

collection = client.get_or_create_collection(
    name="university_knowledge",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)

# Distance threshold — how similar a stored problem must be to return a result.
# Lower = stricter. multi-qa-mpnet is more precise so we can tighten this
# compared to the old model (was 0.55).
MATCH_THRESHOLD = 0.35


def normalize(text: str) -> str:
    """Normalizes text: lowercases, strips, and collapses all whitespace."""
    return " ".join(text.lower().split())


def save_to_library(problem_topic, solution_text, author_name, status, university, location):
    """Saves ANY solution (AI or Student) into the local database with metadata tags."""

    entry_id = str(uuid.uuid4())

    collection.add(
        documents=[problem_topic],
        metadatas=[{
            "solution": solution_text,
            "author":   author_name,
            "status":   status,
            "university": normalize(university),
            "location":   normalize(location)
        }],
        ids=[entry_id]
    )


def search_library(query_topic, university, location):
    """Searches the database for the closest matching solutions."""

    results = collection.query(
        query_texts=[query_topic],
        n_results=3,
        where={"$and": [
            {"university": normalize(university)},
            {"location":   normalize(location)}
        ]}
    )
    return results


def wipe_database():
    """Deletes the entire collection to start fresh."""
    print("Wiping the database clean...")
    client.delete_collection(name="university_knowledge")
    print("Database is now completely empty!")


if __name__ == "__main__":
    wipe_database()