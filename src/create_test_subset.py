import json
import pandas as pd


# =========================
# Configuration
# =========================

INPUT_FILE = "data/support_conversations.csv"
OUTPUT_FILE = "data/test_subset.json"

TEST_SIZE = 10


# =========================
# Load Dataset
# =========================

df = pd.read_csv(INPUT_FILE)


# =========================
# Validate Columns
# =========================

required_columns = [
    "customer_issue",
    "reference_reply"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"Missing required column: {column}"
        )


# =========================
# Create Test Subset
# =========================

test_df = df[
    required_columns
].sample(
    n=min(TEST_SIZE, len(df)),
    random_state=42
)


# =========================
# Convert to JSON
# =========================

test_data = test_df.to_dict(
    orient="records"
)


# =========================
# Save
# =========================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        test_data,
        f,
        indent=4,
        ensure_ascii=False
    )


print(
    f"Created {len(test_data)} test examples."
)

print(
    f"Saved to: {OUTPUT_FILE}"
)