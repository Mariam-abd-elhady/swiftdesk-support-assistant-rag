import os
import json
import time

import pandas as pd
from dotenv import load_dotenv
from google import genai


# =========================
# Configuration
# =========================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"

MODEL_NAME = "gemini-3.6-flash"

DATASET_PATH = "data/support_conversations.csv"
OUTPUT_PATH = "outputs/baseline_outputs.json"

NUM_TEST_EXAMPLES = 10


# =========================
# Gemini Client
# =========================

client = None

if not mock_mode:

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found in .env"
        )

    client = genai.Client(api_key=api_key)


# =========================
# Prompt Styles
# =========================

def zero_shot_prompt(issue):

    return f"""
You are an IT support assistant.

Customer issue:
{issue}

Write a short, clear, polite, and professional support reply.

Do not invent information.
If the issue requires human intervention, recommend escalation.
"""


def few_shot_prompt(issue):

    return f"""
You are an IT support assistant.

Here are examples of good support replies.

Example 1:
Customer issue: I cannot log into my account.

Reply:
Please verify your username and password and try again.
If the issue continues, please contact IT support for further assistance.

Example 2:
Customer issue: My software keeps crashing.

Reply:
Please restart the application and check that you are using the latest version.
If the problem continues, please provide the error message so our support team can investigate.

Now respond to this customer issue:

Customer issue:
{issue}

Write a short, clear, polite, and professional support reply.

Do not invent information.
"""


def reasoned_prompt(issue):

    return f"""
You are an IT support assistant.

Analyze the customer's issue carefully before writing the response.

Consider:
1. What is the main problem?
2. What safe troubleshooting step can be suggested?
3. Does the issue require escalation?
4. Make the response polite, concise, and professional.

Do not reveal your internal reasoning.
Only provide the final support reply.

Customer issue:
{issue}
"""


# =========================
# Mock Response
# =========================

def generate_mock_response(issue, style):

    if style == "zero_shot":

        return (
            "Thank you for contacting IT support. "
            "We have received your request and will review "
            "the issue. Please provide any additional details "
            "or error messages that may help us investigate."
        )

    elif style == "few_shot":

        return (
            "Thank you for contacting IT support. "
            "Please provide any relevant details or error "
            "messages so we can better understand the issue "
            "and assist you. If the problem continues, "
            "our support team can investigate further."
        )

    elif style == "reasoned":

        return (
            "Thank you for contacting IT support. "
            "We understand your concern. Please provide "
            "the relevant details about the issue and any "
            "error messages. Our support team will review "
            "the information and escalate the case if "
            "further assistance is required."
        )

    return "Thank you for contacting IT support."


# =========================
# Generate Response
# =========================

def generate_response(prompt, issue, style):

    # -------------------------
    # Mock Mode
    # -------------------------

    if mock_mode:

        return generate_mock_response(
            issue,
            style
        )

    # -------------------------
    # Real Gemini Mode
    # -------------------------

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


# =========================
# Save Results
# =========================

def save_results(results):

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )


# =========================
# Main
# =========================

def main():

    # -------------------------
    # Load Dataset
    # -------------------------

    df = pd.read_csv(
        DATASET_PATH
    )

    print(
        f"Dataset loaded: {df.shape}"
    )

    # -------------------------
    # Validate Columns
    # -------------------------

    required_columns = [
        "customer_issue",
        "reference_reply"
    ]

    for column in required_columns:

        if column not in df.columns:

            raise ValueError(
                f"Missing required column: {column}"
            )

    # -------------------------
    # Select 10 Examples
    # -------------------------

    test_df = df.head(
        NUM_TEST_EXAMPLES
    )

    results = []

    # -------------------------
    # Process Examples
    # -------------------------

    for position, (index, row) in enumerate(
        test_df.iterrows(),
        start=1
    ):

        issue = str(
            row["customer_issue"]
        )

        reference_reply = str(
            row["reference_reply"]
        )

        print(
            f"\nProcessing example "
            f"{position}/{NUM_TEST_EXAMPLES}..."
        )

        result = {

            "id": int(index),

            "customer_issue": issue,

            "reference_reply": reference_reply,

            "mode": "mock" if mock_mode else "gemini"

        }

        # -------------------------
        # Zero-shot
        # -------------------------

        print(
            "  → Zero-shot"
        )

        result["zero_shot"] = generate_response(
            zero_shot_prompt(issue),
            issue,
            "zero_shot"
        )

        # -------------------------
        # Few-shot
        # -------------------------

        print(
            "  → Few-shot"
        )

        result["few_shot"] = generate_response(
            few_shot_prompt(issue),
            issue,
            "few_shot"
        )

        # -------------------------
        # Reasoned
        # -------------------------

        print(
            "  → Reasoned"
        )

        result["reasoned"] = generate_response(
            reasoned_prompt(issue),
            issue,
            "reasoned"
        )

        # -------------------------
        # Save Immediately
        # -------------------------

        results.append(
            result
        )

        save_results(
            results
        )

        print(
            f"  ✓ Example {position} saved."
        )

    # -------------------------
    # Final Message
    # -------------------------

    print("\n" + "=" * 50)

    print(
        "Experiment completed successfully!"
    )

    print(
        f"Mode: {'MOCK' if mock_mode else 'GEMINI'}"
    )

    print(
        f"Saved {len(results)} examples to:"
    )

    print(
        OUTPUT_PATH
    )

    print("=" * 50)


if __name__ == "__main__":

    main()