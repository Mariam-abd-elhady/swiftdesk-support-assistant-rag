import os
import pandas as pd

from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain_core.documents import Document


# =========================
# Configuration
# =========================

DATASET_PATH = "data/support_conversations.csv"
CHROMA_PATH = "chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# =========================
# Local Embedding Wrapper
# =========================

class LocalEmbeddingFunction:

    def __init__(self, model_name):

        print(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

    def embed_documents(self, texts):

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    def embed_query(self, text):

        embedding = self.model.encode(
            [text],
            normalize_embeddings=True
        )[0]

        return embedding.tolist()


# =========================
# Main
# =========================

def main():

    print("Loading dataset...")

    df = pd.read_csv(
        DATASET_PATH
    )

    print(
        f"Dataset shape: {df.shape}"
    )

    # Validate columns
    required_columns = [
        "customer_issue",
        "reference_reply"
    ]

    for column in required_columns:

        if column not in df.columns:

            raise ValueError(
                f"Missing column: {column}"
            )

    # =========================
    # Create Documents
    # =========================

    documents = []

    for index, row in df.iterrows():

        issue = str(
            row["customer_issue"]
        )

        reply = str(
            row["reference_reply"]
        )

        document = Document(

            page_content=issue,

            metadata={
                "id": int(index),
                "customer_issue": issue,
                "reference_reply": reply
            }
        )

        documents.append(
            document
        )

    print(
        f"Created {len(documents)} documents."
    )

    # =========================
    # Embeddings
    # =========================

    embedding_function = LocalEmbeddingFunction(
        EMBEDDING_MODEL
    )

    # =========================
    # Create Chroma DB
    # =========================

    print(
        "Creating Chroma database..."
    )

    vector_store = Chroma.from_documents(

        documents=documents,

        embedding=embedding_function,

        persist_directory=CHROMA_PATH,

        collection_name="support_tickets"
    )

    print(
        "Chroma database created successfully!"
    )

    print(
        f"Saved to: {CHROMA_PATH}"
    )

    # =========================
    # Test Retrieval
    # =========================

    test_query = (
        "I cannot login to my account"
    )

    print(
        f"\nTesting retrieval:"
    )

    print(
        f"Query: {test_query}"
    )

    results = vector_store.similarity_search(
        test_query,
        k=3
    )

    print(
        "\nTop 3 similar tickets:"
    )

    for i, document in enumerate(
        results,
        start=1
    ):

        print(
            f"\n--- Result {i} ---"
        )

        print(
            "Issue:",
            document.page_content
        )

        print(
            "Reply:",
            document.metadata[
                "reference_reply"
            ]
        )


if __name__ == "__main__":

    main()