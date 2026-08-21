# SwiftDesk IT Support Assistant


## RAG Capstone Project


SwiftDesk is a Generative AI-powered IT support assistant that helps
support agents create short draft responses to customer support tickets.


The system uses Retrieval-Augmented Generation (RAG) to retrieve similar
previous support tickets from a local Chroma vector database and uses
them as context when generating a response.


All AI-generated responses must be reviewed by a human support agent
before being sent to the customer.


---


## Project Features


- Retrieval-Augmented Generation (RAG)
- Local Chroma vector database
- Sentence Transformer embeddings
- Google Gemini API integration
- FastAPI REST backend
- Streamlit frontend
- Zero-shot prompting
- Few-shot prompting
- Reasoned prompting
- RAG ON/OFF
- Configurable number of retrieved examples
- ROUGE-L evaluation
- Responsible AI configuration
- Human-in-the-loop review
- MOCK_MODE for classroom/offline demonstration


---


## Technologies


- Python 3
- Google Gemini API
- LangChain
- Chroma DB
- Sentence Transformers
- FastAPI
- Uvicorn
- Streamlit
- Pandas
- ROUGE-L
- python-dotenv
- YAML


---


## Project Structure


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
│   ├── raw/
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
├── chroma_db/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```


Note: The .env file is intentionally not included in the project
structure because it contains the private Gemini API key and should
never be committed to version control.

Installation

Clone or download the project and open a terminal in the project
directory.

Install the required dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file in the project root.

For Gemini API usage:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
MOCK_MODE=false

For an offline classroom demonstration:

GEMINI_API_KEY=
MOCK_MODE=true

Never commit the real .env file or expose the Gemini API key.

The .env.example file can be used as a template.

Prepare the Dataset

The dataset preparation script converts the raw support ticket data
into the normalized project dataset.

Run:

python src/prepare_kaggle_dataset.py

The normalized dataset is saved as:

data/support_conversations.csv
Create the Test Subset

The project uses a small test subset for evaluation.

Create the test subset using:

python src/create_test_subset.py

The test file is saved as:

data/test_subset.json
Create the Chroma Database

Run the ingestion script:

python src/ingest_chroma.py

This creates the local Chroma vector database:

chroma_db/

The support tickets are converted into embeddings and stored locally
for similarity-based retrieval.

Run the FastAPI Backend

Start the backend using:

uvicorn backend.main:app --reload

The API will be available at:

http://127.0.0.1:8000
Health Check

Endpoint:

GET /health

Example response:

{
    "status": "ok",
    "service": "SwiftDesk IT Support Assistant"
}
Generate Support Reply

Endpoint:

POST /generate

The endpoint accepts:

Customer issue
Prompt style
RAG ON/OFF
Number of retrieved examples
Run the Streamlit Frontend

Open another terminal and run:

streamlit run frontend/app.py

The frontend allows the user to:

Enter a customer issue.
Select a prompt style.
Enable or disable RAG.
Select the number of retrieved examples.
Generate an AI draft.
View retrieved sources.
Review the response before sending.
Prompt Styles
Zero-shot

Generates a concise support response without demonstrations.

Few-shot

Uses retrieved previous support examples as guidance when generating
the response.

Reasoned

The system analyzes the issue internally and returns only the final
support response without exposing internal reasoning.

RAG Workflow

The project follows these steps:

Customer Issue
      ↓
Create Query Embedding
      ↓
Search Chroma DB
      ↓
Retrieve Similar Support Tickets
      ↓
Build Prompt
      ↓
Generate AI Draft
      ↓
Human Review
      ↓
Final Support Response
Evaluation

The project uses 10 test examples for evaluation.

Create the test subset:

python src/create_test_subset.py

Run the evaluation:

python src/evaluation_script.py

The results are saved to:

outputs/evaluation_results.json
Current Evaluation Result
Number of test examples: 10
Average ROUGE-L: 0.1150

The current evaluation was performed using MOCK_MODE.

Therefore, the ROUGE-L result demonstrates that the evaluation
pipeline is functioning, but it should not be interpreted as the
expected quality of the Gemini-generated system.

Responsible AI

Responsible AI rules are stored in:

config/RAI_Config.yaml

The system addresses:

Accuracy
Respectful language
Privacy
Risk escalation
Transparency
Mandatory human review
Human Review

The AI response is a draft and must not be sent automatically.

A human support agent should verify that the response is:

Clear
Relevant
Polite
Accurate
Safe

Cases involving security risks, sensitive information, data loss,
or other risky situations should be escalated to a human agent.

Limitations
The evaluation dataset is small.
ROUGE-L does not fully measure support response quality.
MOCK_MODE produces a generic response.
Retrieved examples may not always provide the exact solution.
Human review remains necessary.
Gemini API usage may be affected by API limits or availability.
The system is designed for response drafting rather than fully
autonomous customer support.
Responsible Use

SwiftDesk is designed as a human-in-the-loop support assistant.

It should assist support agents with first-draft generation rather
than operate as a fully autonomous customer support system.

Human agents remain responsible for verifying and approving the final
response.

Project Deliverables

The project includes:

task_description.html
FastAPI backend
Streamlit frontend
RAG pipeline
Chroma vector database
Dataset preparation scripts
Prompt experiments
Evaluation script
Evaluation results
Responsible AI configuration
Final project report
Requirements file
Environment variable template
Conclusion

SwiftDesk demonstrates a complete local RAG workflow for IT support
response drafting, combining retrieval, prompt engineering, Gemini
generation, API development, interactive frontend usage, evaluation,
and Responsible AI practices.

The system is intended to help human support agents work more
efficiently while keeping human review as a mandatory part of the
response process.
