from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.rag_chain import generate_support_reply


# =========================
# FastAPI App
# =========================

app = FastAPI(
    title="SwiftDesk IT Support Assistant",
    description="RAG-based IT support response drafting assistant",
    version="1.0.0"
)


# =========================
# Request Model
# =========================

class GenerateRequest(BaseModel):

    customer_issue: str = Field(
        ...,
        min_length=3,
        description="Customer IT support issue"
    )

    prompt_style: str = Field(
        default="zero_shot",
        description="Prompt style: zero_shot, few_shot, or reasoned"
    )

    rag_enabled: bool = Field(
        default=True,
        description="Enable or disable RAG retrieval"
    )

    num_retrieved: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of retrieved examples"
    )


# =========================
# Health Check
# =========================

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "SwiftDesk IT Support Assistant"
    }


# =========================
# Generate Response
# =========================

@app.post("/generate")
def generate_response(request: GenerateRequest):

    allowed_styles = [
        "zero_shot",
        "few_shot",
        "reasoned"
    ]

    if request.prompt_style not in allowed_styles:

        raise HTTPException(
            status_code=400,
            detail=(
                "prompt_style must be one of: "
                "zero_shot, few_shot, reasoned"
            )
        )

    try:

        result = generate_support_reply(

            customer_issue=request.customer_issue,

            prompt_style=request.prompt_style,

            rag_enabled=request.rag_enabled,

            num_retrieved=request.num_retrieved
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Run directly
# =========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )