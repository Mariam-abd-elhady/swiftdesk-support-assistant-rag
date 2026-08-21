# SwiftDesk IT Support Assistant
## Final Project Report

---

## 1. Project Overview

SwiftDesk is a local Retrieval-Augmented Generation (RAG) system
designed to help IT support agents draft short customer responses.

The system accepts a customer support issue, retrieves similar
previous support tickets from a local Chroma vector database, and
uses the retrieved examples as context for response generation.

The generated response is treated as a draft and must be reviewed
by a human support agent before being sent to the customer.

---

## 2. Technologies Used

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
- YAML configuration

---

## 3. System Workflow

The system follows this workflow:

Customer Issue
      ↓
Input through Streamlit
      ↓
FastAPI /generate
      ↓
RAG Retrieval
      ↓
Chroma Vector Database
      ↓
Similar Previous Support Tickets
      ↓
Prompt Construction
      ↓
Gemini / Mock Generation
      ↓
AI Draft Response
      ↓
Human Review
      ↓
Final Support Response

---

## 4. Dataset Preparation

The Kaggle customer support dataset was converted into a smaller
project-specific dataset containing two main fields:

- customer_issue
- reference_reply

A test subset containing 10 examples was created for evaluation.

The smaller dataset was selected to keep local processing and
Chroma retrieval practical on a normal laptop.

---

## 5. RAG Design

Previous customer support examples were converted into vector
representations using a local Sentence Transformer embedding model.

The embeddings were stored in a local Chroma database.

For a new customer issue, the system retrieves the most similar
previous support examples.

The retrieved examples contain:

- Previous customer issue
- Approved/reference support reply
- Example ID

These examples are then included in the prompt as contextual
guidance.

The system supports both:

- RAG ON
- RAG OFF

This allows the effect of retrieval to be tested.

---

## 6. Prompt Engineering

Three prompt styles were implemented:

### Zero-shot

The model is asked to generate a concise professional support reply
without relying on demonstrations.

### Few-shot

The model receives retrieved previous support examples and uses them
as guidance for generating the response.

### Reasoned

The system instructs the model to analyze the issue internally and
produce only the final support response without exposing internal
reasoning.

All prompt styles include rules for:

- Professional language
- Conciseness
- Accuracy
- Privacy
- Safe escalation
- Human review

---

## 7. Functional Testing

The Streamlit frontend was tested successfully using the following
configurations:

| Test | Result |
|---|---|
| Zero-shot + RAG ON | PASS |
| Few-shot + RAG ON | PASS |
| Reasoned + RAG ON | PASS |
| Few-shot + RAG OFF | PASS |
| RAG ON + 1 retrieved source | PASS |
| RAG ON + 5 retrieved sources | PASS |

The tests confirmed that the frontend correctly communicates the
selected prompt style, RAG setting, and retrieval count to the
backend.

---

## 8. Evaluation

Ten test examples were evaluated using ROUGE-L against their
reference replies.

Evaluation configuration:

- Test examples: 10
- Prompt style: Few-shot
- RAG: ON
- Retrieved examples: 3

Average ROUGE-L:

**0.1150**

The evaluation pipeline successfully generated responses, compared
them with reference replies, calculated ROUGE-L, and saved the
results to `outputs/evaluation_results.json`.

### Evaluation Limitation

The current classroom evaluation was performed using MOCK_MODE.
The mock implementation returns a generic fallback response rather
than a dynamically generated Gemini response.

Therefore, the ROUGE-L score of 0.1150 should not be interpreted as
the expected quality of the production Gemini-based system.

The result mainly demonstrates that the evaluation pipeline is
working correctly.

---

## 9. Manual Review

Five generated responses were manually reviewed using the following
criteria:

- Clear
- Relevant
- Polite
- Accurate
- Safe

### Manual Review Findings

The generated responses were generally:

- Clear
- Polite
- Safe

However, relevance was limited because the mock response was generic
and repeated across different support issues.

Accuracy was therefore considered acceptable only as a generic
acknowledgment, rather than as a complete solution to each specific
customer problem.

This demonstrates the importance of using the actual generative
model and maintaining human review before sending responses.

---

## 10. Responsible AI

The project includes a Responsible AI configuration in:

`config/RAI_Config.yaml`

The system follows these principles:

### Accuracy

The assistant should not invent technical facts or customer
information.

### Respectful Language

Responses should remain polite, professional, and easy to understand.

### Risk Escalation

Security-sensitive, risky, or complex cases should be escalated to
a human support agent.

### Privacy

The assistant should not expose passwords, authentication codes,
private credentials, or unnecessary personal information.

### Human Review

Every generated response must be reviewed by a human support agent
before being sent to the customer.

### Transparency

The generated response is clearly presented as an AI draft.

---

## 11. Limitations

The current system has several limitations:

1. The evaluation dataset is small.
2. ROUGE-L alone cannot fully measure support response quality.
3. MOCK_MODE produces generic responses.
4. Retrieved examples may not always contain the exact solution.
5. Human review is still required.
6. Gemini API availability and usage limits may affect deployment.
7. The system should not be treated as an autonomous support agent.

---

## 12. Conclusion

The SwiftDesk IT Support Assistant demonstrates a complete local RAG
workflow for IT support response drafting.

The project includes dataset preparation, embeddings, Chroma
retrieval, prompt engineering, FastAPI backend integration,
Streamlit frontend interaction, automated evaluation, manual review,
and Responsible AI practices.

The system is designed as a human-in-the-loop assistant rather than
an autonomous support system.

The main goal is to reduce the time required to create first-draft
support responses while keeping a human support agent responsible
for the final response.