
import os
import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai

load_dotenv()

# Gemini API setup
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

gemini_client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("study_documents")


def retrieve_documents(question, top_k=4):

    if collection.count() == 0:
        return []

    # Convert question into embedding
    question_embedding = embedding_model.encode(
        question,
        convert_to_numpy=True
    ).tolist()

    # Search for similar chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count())
    )

    retrieved = []

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]

        retrieved.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"]
        })

    return retrieved


def generate_answer(question, use_rag=True):

    context = ""
    retrieved = []

    if use_rag:

        retrieved = retrieve_documents(question)

        if not retrieved:
            return {
                "answer": "No relevant documents were found.",
                "sources": []
            }

        for item in retrieved:
            context += (
                f"\nSource: {item['source']}, "
                f"Page: {item['page']}\n"
                f"{item['text']}\n"
            )

        prompt = f"""
        You are a helpful study assistant.

        Answer the user's question using ONLY the
        following retrieved document context.

        If the answer is not available in the context,
        clearly say that the documents do not contain
        enough information.

        Retrieved Context:
        {context}

        User Question:
        {question}

        Give a clear and simple answer.
        """

    else:

        prompt = f"""
        You are a helpful AI assistant.

        Answer this question using your general
        knowledge. You have NOT been given any
        uploaded document context.

        Question: {question}
        """

    try:

        response = gemini_client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return {
            "answer": response.text or "No answer generated.",
            "sources": [
                {
                    "source": item["source"],
                    "page": item["page"]
                }
                for item in retrieved
            ]
        }

    except Exception as error:

        print("Gemini API Error:", error)

        return {
            "answer": "AI service is temporarily unavailable. Please try again.",
            "sources": []
        }
