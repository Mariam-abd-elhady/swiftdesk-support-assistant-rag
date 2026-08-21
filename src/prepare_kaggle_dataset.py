import pandas as pd
from pathlib import Path


# =========================
# Paths
# =========================

INPUT_FILE = Path(
    "data/raw/dataset/dataset-tickets-multi-lang-4-20k.csv"
)

OUTPUT_FILE = Path(
    "data/support_conversations.csv"
)


# =========================
# Load dataset
# =========================

df = pd.read_csv(INPUT_FILE)

print(f"Original dataset shape: {df.shape}")


# =========================
# Keep English tickets
# =========================

df = df[df["language"] == "en"].copy()

print(f"English tickets: {len(df)}")


# =========================
# Keep required columns
# =========================

df = df[["body", "answer"]].copy()

df = df.rename(
    columns={
        "body": "customer_issue",
        "answer": "reference_reply"
    }
)


# =========================
# Remove missing values
# =========================

df = df.dropna(
    subset=["customer_issue", "reference_reply"]
)


# =========================
# Clean text
# =========================

df["customer_issue"] = (
    df["customer_issue"]
    .astype(str)
    .str.replace(r"\\n", "\n", regex=True)
    .str.strip()
)

df["reference_reply"] = (
    df["reference_reply"]
    .astype(str)
    .str.replace(r"\\n", "\n", regex=True)
    .str.strip()
)


# =========================
# Remove empty text
# =========================

df = df[
    (df["customer_issue"].str.len() > 0)
    & (df["reference_reply"].str.len() > 0)
]


# =========================
# Select project subset
# =========================

df = df.head(1000)


# =========================
# Save normalized dataset
# =========================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# =========================
# Summary
# =========================

print(f"Final dataset shape: {df.shape}")
print(f"Saved to: {OUTPUT_FILE}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst example:")
print("\nCustomer issue:")
print(df.iloc[0]["customer_issue"])

print("\nReference reply:")
print(df.iloc[0]["reference_reply"])