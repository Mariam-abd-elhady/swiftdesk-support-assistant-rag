````markdown
##🤖 SwiftDesk IT Support Assistant

## RAG Capstone Project | Generative AI + Retrieval-Augmented Generation

SwiftDesk is a Generative AI-powered IT support assistant designed to help support agents create concise, professional, and context-aware draft responses to customer support tickets.

The system uses **Retrieval-Augmented Generation (RAG)** to retrieve similar historical support tickets from a local **Chroma vector database** and use them as context when generating a response.

> ⚠️ **Human-in-the-Loop:** AI-generated responses are drafts only. A human support agent must review and approve every response before it is sent to a customer.

---

## ✨ Key Features

- 🔎 Retrieval-Augmented Generation (RAG)
- 🧠 Sentence Transformer embeddings
- 🗄️ Local Chroma vector database
- 🤖 Google Gemini API integration
- ⚡ FastAPI REST backend
- 🎨 Streamlit interactive frontend
- 📝 Zero-shot prompting
- 🎯 Few-shot prompting
- 🧩 Reasoned prompting
- 🔄 RAG ON / OFF
- 📚 Configurable number of retrieved examples
- 📊 ROUGE-L evaluation
- 🛡️ Responsible AI configuration
- 👤 Human-in-the-loop review
- 📴 MOCK_MODE for offline/classroom demonstrations

---

## 🏗️ System Architecture

```text
                ┌──────────────────────┐
                │   Customer Support   │
                │       Ticket         │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Query Embedding    │
                │ Sentence Transformer │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Chroma Vector     │
                │      Database        │
                └──────────┬───────────┘
                           │
                    Similar Tickets
                           │
                           ▼
                ┌──────────────────────┐
                │    RAG Prompt        │
                │ Construction         │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Gemini Model      │
                │   Response Drafting  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    AI Draft Reply    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Human Review      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Final Response     │
                └──────────────────────┘
````

---

## 🛠️ Technologies

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Core development             |
| Google Gemini         | Generative AI                |
| LangChain             | RAG integration              |
| Chroma DB             | Vector storage and retrieval |
| Sentence Transformers | Local text embeddings        |
| FastAPI               | Backend REST API             |
| Uvicorn               | ASGI server                  |
| Streamlit             | Interactive frontend         |
| Pandas                | Dataset processing           |
| ROUGE-L               | Response evaluation          |
| python-dotenv         | Environment configuration    |
| YAML                  | Responsible AI configuration |

---

## 📁 Project Structure

```text
swiftdesk-support-assistant-rag/
│
├── task_description.html
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── src/
│   ├── settings.py
│   ├── prompts.py
│   ├── rag_chain.py
│   ├── ingest_chroma.py
│   ├── prepare_kaggle_dataset.py
│   ├── gemini_basics.py
│   ├── evaluation_script.py
│   └── create_test_subset.py
│
├── data/
│   ├── support_conversations.csv
│   └── test_subset.json
│
├── config/
│   └── RAI_Config.yaml
│
├── outputs/
│   ├── baseline_outputs.json
│   ├── evaluation_results.json
│   └── final_report.md
│
├── .gitignore
├── requirements.txt
└── README.md
```

> 🔐 The `.env` file is intentionally excluded from the repository because it contains the private Gemini API key.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/Mariamabdelhady/swiftdesk-support-assistant-rag.git
cd swiftdesk-support-assistant-rag
```

---

## 2. Install Dependencies

Create a virtual environment if desired:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root.

### Gemini API Mode

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
MOCK_MODE=false
```

### Offline / Classroom Mode

```env
GEMINI_API_KEY=
MOCK_MODE=true
```

> 🔒 Never commit your real Gemini API key to GitHub.

---

# 📊 Dataset Preparation

The project includes a dataset preparation pipeline that converts the raw support ticket data into the normalized project dataset.

Run:

```bash
python src/prepare_kaggle_dataset.py
```

The processed dataset will be saved as:

```text
data/support_conversations.csv
```

---

# 🗂️ Create the Test Dataset

The evaluation pipeline uses a small test subset containing **10 support examples**.

Create it with:

```bash
python src/create_test_subset.py
```

Output:

```text
data/test_subset.json
```

---

# 🧠 Build the Chroma Vector Database

Create the local vector database by running:

```bash
python src/ingest_chroma.py
```

This process:

1. Loads the processed support tickets.
2. Creates text embeddings using Sentence Transformers.
3. Stores the embeddings in Chroma.
4. Enables similarity-based ticket retrieval.

The vector database is stored locally in:

```text
chroma_db/
```

---

# ⚡ Run the Backend

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Health Check

```http
GET /health
```

Example response:

```json
{
    "status": "ok",
    "service": "SwiftDesk IT Support Assistant"
}
```

### Generate Support Reply

```http
POST /generate
```

The endpoint supports:

* Customer issue
* Prompt style
* RAG ON / OFF
* Number of retrieved examples

---

# 🎨 Run the Streamlit Frontend

Open a second terminal and run:

```bash
streamlit run frontend/app.py
```

The frontend allows support agents to:

1. Enter a customer support issue.
2. Select a prompting strategy.
3. Enable or disable RAG.
4. Select the number of retrieved examples.
5. Generate an AI draft response.
6. View retrieved support examples.
7. Review the generated response before sending.

---

# 📝 Prompting Strategies

## Zero-Shot

Generates a concise support response without providing demonstrations.

## Few-Shot

Uses retrieved historical support examples as guidance for generating the response.

## Reasoned

The system analyzes the issue internally and returns only the final support response without exposing internal reasoning.

---

# 🔎 RAG Workflow

The complete RAG pipeline follows this process:

```text
Customer Issue
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
Retrieve Similar Tickets
      ↓
Build RAG Prompt
      ↓
Generate AI Draft
      ↓
Human Review
      ↓
Final Support Response
```

---

# 📈 Evaluation

The project includes an automated evaluation pipeline using **ROUGE-L**.

Run:

```bash
python src/evaluation_script.py
```

Results are saved to:

```text
outputs/evaluation_results.json
```

### Current Evaluation

| Metric            |   Result |
| ----------------- | -------: |
| Test Examples     |       10 |
| Average ROUGE-L   |   0.1150 |
| Prompt Style      | Few-Shot |
| RAG               |  Enabled |
| Retrieved Sources |        3 |
| Mode              |     MOCK |

> **Important:** The current evaluation was performed using `MOCK_MODE=true`. The mock response is intentionally generic, so the ROUGE-L score mainly demonstrates that the evaluation pipeline is functioning. It should not be interpreted as the expected quality of the Gemini-powered system.

---

# 🛡️ Responsible AI

Responsible AI rules are defined in:

```text
config/RAI_Config.yaml
```

The project addresses:

* **Accuracy** — avoid unsupported or fabricated information.
* **Respectful Language** — maintain professional communication.
* **Privacy** — avoid exposing sensitive information.
* **Risk Escalation** — recommend human intervention for risky cases.
* **Transparency** — clearly identify generated content as a draft.
* **Human Oversight** — require human review before sending responses.

---

# 👤 Human-in-the-Loop

SwiftDesk is designed as an **AI-assisted support system**, not a fully autonomous customer support agent.

Every generated response should be reviewed by a support agent for:

* ✅ Clarity
* ✅ Relevance
* ✅ Politeness
* ✅ Accuracy
* ✅ Safety

Issues involving security risks, sensitive information, potential data loss, or other high-risk situations should be escalated to a human support agent.

---

# ⚠️ Limitations

* The evaluation dataset contains only 10 test examples.
* ROUGE-L does not fully measure the quality of customer support responses.
* `MOCK_MODE` produces a generic response and is intended for demonstration/testing.
* Retrieved examples may not always contain the exact solution required.
* Gemini API availability and usage may be affected by API limits.
* Human review remains necessary.
* The system is designed for **response drafting**, not autonomous customer support.

---

# 📦 Project Deliverables

The project includes:

* `task_description.html`
* FastAPI backend
* Streamlit frontend
* RAG pipeline
* Chroma vector database
* Dataset preparation scripts
* Prompting experiments
* Evaluation script
* Evaluation results
* Responsible AI configuration
* Final project report
* Requirements file
* Git configuration

---

# 📄 Final Report

The final project report is available at:

```text
outputs/final_report.md
```

It contains the project evaluation and key findings.

---

# 🔐 Security

The project follows basic secret-management practices:

* API keys are stored in `.env`.
* `.env` is excluded using `.gitignore`.
* Raw datasets are excluded from version control.
* Local Chroma database files are excluded from version control.
* Real API credentials must never be committed to GitHub.

---

# 🎯 Responsible Use

SwiftDesk is intended to **assist human support agents** by generating first-draft responses based on similar historical support cases.

It should not replace human judgment.

The final responsibility for approving and sending a customer response remains with the human support agent.

---

# 🏁 Conclusion

SwiftDesk demonstrates a complete **Retrieval-Augmented Generation workflow** for IT support response drafting.

The project combines:

**Data Preparation → Embeddings → Vector Retrieval → RAG → Prompt Engineering → Gemini Generation → API Development → Interactive Frontend → Evaluation → Responsible AI**

The system provides a practical example of how Generative AI and RAG can be integrated into a human-in-the-loop IT support workflow while maintaining safety, transparency, and human oversight.

---

## 👩‍💻 Author

**Mariam Abdelhady Ramadan**

AI & Data Science | Backend & AI Systems

---

⭐ If you find this project useful, feel free to explore the repository and its implementation.

````
