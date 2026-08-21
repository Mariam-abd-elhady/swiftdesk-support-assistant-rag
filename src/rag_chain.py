import os

from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma


# =========================
# Configuration
# =========================

load_dotenv()

MOCK_MODE = os.getenv(
    "MOCK_MODE",
    "false"
).lower() == "true"

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

MODEL_NAME = "gemini-3.6-flash"

CHROMA_PATH = "chroma_db"

COLLECTION_NAME = "support_tickets"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# =========================
# Clients
# =========================

gemini_client = None

if not MOCK_MODE:

    if not GEMINI_API_KEY:

        raise ValueError(
            "GEMINI_API_KEY not found in .env"
        )

    gemini_client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# =========================
# Local Embeddings
# =========================

class LocalEmbeddingFunction:

    def __init__(
        self,
        model_name=EMBEDDING_MODEL
    ):

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
# Load Chroma
# =========================

def get_vector_store():

    embedding_function = (
        LocalEmbeddingFunction()
    )

    vector_store = Chroma(

        persist_directory=CHROMA_PATH,

        collection_name=COLLECTION_NAME,

        embedding_function=embedding_function
    )

    return vector_store


# =========================
# Retrieve Similar Tickets
# =========================

def retrieve_examples(
    customer_issue,
    k=3
):

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        customer_issue,
        k=k
    )

    examples = []

    for document in documents:

        examples.append({

            "customer_issue":
                document.metadata.get(
                    "customer_issue",
                    document.page_content
                ),

            "reference_reply":
                document.metadata.get(
                    "reference_reply",
                    ""
                ),

            "id":
                document.metadata.get(
                    "id"
                )
        })

    return examples


# =========================
# Build RAG Prompt
# =========================

def build_rag_prompt(
    customer_issue,
    retrieved_examples,
    prompt_style="zero_shot"
):

    context = ""

    for i, example in enumerate(
        retrieved_examples,
        start=1
    ):

        context += f"""
Example {i}

Customer issue:
{example["customer_issue"]}

Approved support reply:
{example["reference_reply"]}

"""


    if prompt_style == "few_shot":

        instruction = """
Use the retrieved examples as guidance.
Follow their helpful style, but do not copy
irrelevant information.
"""

    elif prompt_style == "reasoned":

        instruction = """
Analyze the customer's issue internally.
Identify the main problem and the safest
appropriate support response.
Do not reveal your internal reasoning.
Only provide the final reply.
"""

    else:

        instruction = """
Write a concise and professional support reply.
"""


    prompt = f"""
You are SwiftDesk IT Support Assistant.

Your task is to draft a short support response
for a customer.

{instruction}

Retrieved previous support examples:
{context}

Current customer issue:
{customer_issue}

Rules:

- Be polite and professional.
- Be concise.
- Do not invent facts.
- Do not expose private information.
- Do not promise something you cannot guarantee.
- If the issue is risky or requires human intervention,
  recommend escalation.
- The final response should be suitable for review
  by a human support agent.

Write ONLY the draft support reply.
"""

    return prompt.strip()


# =========================
# Mock Response
# =========================

def generate_mock_reply(
    customer_issue,
    retrieved_examples,
    prompt_style
):

    if retrieved_examples:

        first_reply = retrieved_examples[0][
            "reference_reply"
        ]

        return (
            "Thank you for contacting SwiftDesk Support. "
            "Based on similar previous support cases, "
            "please review the suggested troubleshooting "
            "steps and provide any relevant error message "
            "if the issue continues. Our support team can "
            "investigate further if needed."
        )

    return (
        "Thank you for contacting SwiftDesk Support. "
        "We have received your request and will review "
        "the issue. Please provide any additional details "
        "or error messages that may help us investigate."
    )


# =========================
# Generate with Gemini
# =========================

def generate_with_gemini(prompt):

    response = gemini_client.models.generate_content(

        model=MODEL_NAME,

        contents=prompt
    )

    return response.text.strip()


# =========================
# Main RAG Function
# =========================

def generate_support_reply(
    customer_issue,
    prompt_style="zero_shot",
    rag_enabled=True,
    num_retrieved=3
):

    # -------------------------
    # Retrieval
    # -------------------------

    retrieved_examples = []

    if rag_enabled:

        retrieved_examples = retrieve_examples(
            customer_issue,
            k=num_retrieved
        )

    # -------------------------
    # Build Prompt
    # -------------------------

    prompt = build_rag_prompt(

        customer_issue,

        retrieved_examples,

        prompt_style
    )

    # -------------------------
    # Generate
    # -------------------------

    if MOCK_MODE:

        reply = generate_mock_reply(

            customer_issue,

            retrieved_examples,

            prompt_style
        )

    else:

        reply = generate_with_gemini(
            prompt
        )

    # -------------------------
    # Return Result
    # -------------------------

    return {

        "reply": reply,

        "retrieved_sources":
            retrieved_examples,

        "prompt_style":
            prompt_style,

        "rag_enabled":
            rag_enabled,

        "num_retrieved":
            len(retrieved_examples),

        "mode":
            "mock" if MOCK_MODE
            else "gemini"
    }


# =========================
# Simple Test
# =========================

if __name__ == "__main__":

    test_issue = (
        "I cannot login to my account"
    )

    result = generate_support_reply(

        customer_issue=test_issue,

        prompt_style="few_shot",

        rag_enabled=True,

        num_retrieved=3
    )

    print("\n" + "=" * 60)

    print("Generated Reply:")

    print(result["reply"])

    print("\nRetrieved Sources:")

    for i, source in enumerate(
        result["retrieved_sources"],
        start=1
    ):

        print(
            f"\n--- Source {i} ---"
        )

        print(
            "Issue:",
            source["customer_issue"]
        )

        print(
            "Reply:",
            source["reference_reply"]
        )

    print("\nMode:", result["mode"])

    print("=" * 60)