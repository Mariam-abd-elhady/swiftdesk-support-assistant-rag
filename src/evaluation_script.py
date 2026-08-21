import json
import os
from pathlib import Path

from rouge_score import rouge_scorer

from src.rag_chain import generate_support_reply


# =========================
# Configuration
# =========================

TEST_FILE = "data/test_subset.json"
OUTPUT_FILE = "outputs/evaluation_results.json"

ROUGE_TYPE = "rougeL"


# =========================
# Load Test Data
# =========================

def load_test_data():

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# Calculate ROUGE-L
# =========================

def calculate_rouge_l(
    reference,
    generated
):

    scorer = rouge_scorer.RougeScorer(
        [ROUGE_TYPE],
        use_stemmer=True
    )

    scores = scorer.score(
        reference,
        generated
    )

    return scores["rougeL"].fmeasure


# =========================
# Run Evaluation
# =========================

def run_evaluation():

    test_data = load_test_data()

    results = []

    scores = []


    for index, item in enumerate(
        test_data,
        start=1
    ):

        customer_issue = item[
            "customer_issue"
        ]

        reference_reply = item[
            "reference_reply"
        ]


        # Generate response

        output = generate_support_reply(

            customer_issue=customer_issue,

            prompt_style="few_shot",

            rag_enabled=True,

            num_retrieved=3
        )


        generated_reply = output[
            "reply"
        ]


        # Calculate ROUGE-L

        rouge_l = calculate_rouge_l(

            reference_reply,

            generated_reply
        )


        scores.append(
            rouge_l
        )


        results.append({

            "test_id": index,

            "customer_issue":
                customer_issue,

            "reference_reply":
                reference_reply,

            "generated_reply":
                generated_reply,

            "rougeL":
                round(rouge_l, 4)

        })


        print(
            f"Test {index}/"
            f"{len(test_data)} "
            f"- ROUGE-L: "
            f"{rouge_l:.4f}"
        )


    # =========================
    # Calculate Average
    # =========================

    average_rouge_l = (
        sum(scores) / len(scores)
        if scores
        else 0
    )


    # =========================
    # Final Output
    # =========================

    evaluation_output = {

        "num_test_examples":
            len(test_data),

        "prompt_style":
            "few_shot",

        "rag_enabled":
            True,

        "num_retrieved":
            3,

        "average_rougeL":
            round(
                average_rouge_l,
                4
            ),

        "results":
            results

    }


    # =========================
    # Save Results
    # =========================

    os.makedirs(
        "outputs",
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            evaluation_output,
            f,
            indent=4,
            ensure_ascii=False
        )


    print(
        "\nEvaluation completed."
    )

    print(
        f"Average ROUGE-L: "
        f"{average_rouge_l:.4f}"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


# =========================
# Main
# =========================

if __name__ == "__main__":

    run_evaluation()