import streamlit as st
import requests


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="SwiftDesk IT Support Assistant",
    page_icon="🛠️",
    layout="wide"
)


# =========================
# API Configuration
# =========================

API_URL = "http://127.0.0.1:8000"


# =========================
# Header
# =========================

st.title("🛠️ SwiftDesk IT Support Assistant")

st.markdown(
    """
    **AI-powered IT Support Response Drafting**

    The assistant uses **RAG + Gemini** to retrieve similar
    support tickets and generate a draft response.
    """
)

st.warning(
    "⚠️ Human Review Required: "
    "The generated response is only a draft. "
    "A human support agent must review it before sending."
)


# =========================
# Customer Issue
# =========================

st.subheader("🎫 Customer Issue")

customer_issue = st.text_area(
    "Enter the customer's IT support issue:",
    placeholder=(
        "Example: I cannot log into my account even after "
        "resetting my password."
    ),
    height=160
)


# =========================
# Generation Settings
# =========================

st.subheader("⚙️ Generation Settings")

col1, col2, col3 = st.columns(3)


with col1:

    prompt_style = st.selectbox(
        "Prompt Style",
        options=[
            "zero_shot",
            "few_shot",
            "reasoned"
        ],
        format_func=lambda x: {
            "zero_shot": "Zero-shot",
            "few_shot": "Few-shot",
            "reasoned": "Reasoned"
        }[x]
    )


with col2:

    rag_enabled = st.toggle(
        "Enable RAG",
        value=True
    )


with col3:

    num_retrieved = st.slider(
        "Retrieved Examples",
        min_value=1,
        max_value=10,
        value=3
    )


# =========================
# Generate Button
# =========================

if st.button(
    "🚀 Generate Support Draft",
    use_container_width=True
):

    if not customer_issue.strip():

        st.warning(
            "Please enter a customer issue first."
        )

    else:

        payload = {
            "customer_issue": customer_issue,
            "prompt_style": prompt_style,
            "rag_enabled": rag_enabled,
            "num_retrieved": num_retrieved
        }

        try:

            with st.spinner(
                "🔄 Generating support response..."
            ):

                response = requests.post(
                    f"{API_URL}/generate",
                    json=payload,
                    timeout=60
                )


            # =========================
            # Successful Response
            # =========================

            if response.status_code == 200:

                result = response.json()


                # =========================
                # AI Draft
                # =========================

                st.subheader("🤖 AI Draft Response")

                draft = result.get(
                    "reply",
                    result.get(
                        "draft",
                        "No response generated."
                    )
                )

                st.success(draft)


                # =========================
                # Human Review
                # =========================

                st.warning(
                    """
                    👤 **Human Review Required**

                    Before sending this response, the support agent
                    should verify that it is:

                    - Clear
                    - Relevant
                    - Polite
                    - Accurate
                    - Safe
                    """
                )


                # =========================
                # RAG Information
                # =========================

                st.subheader("📚 Retrieved Sources")


                if not rag_enabled:

                    st.info(
                        "RAG is disabled. No support examples "
                        "were retrieved."
                    )

                else:

                    sources = result.get(
                        "retrieved_sources",
                        result.get(
                            "sources",
                            []
                        )
                    )


                    if sources:

                        for i, source in enumerate(
                            sources,
                            start=1
                        ):

                            with st.expander(
                                f"📄 Retrieved Source {i}"
                            ):

                                if isinstance(
                                    source,
                                    dict
                                ):

                                    customer = source.get(
                                        "customer_issue",
                                        "N/A"
                                    )

                                    reply = source.get(
                                        "reference_reply",
                                        "N/A"
                                    )

                                    st.markdown(
                                        "**Customer Issue:**"
                                    )

                                    st.write(customer)

                                    st.markdown(
                                        "**Reference Reply:**"
                                    )

                                    st.write(reply)

                                else:

                                    st.write(source)

                    else:

                        st.info(
                            "No retrieved sources were returned "
                            "by the backend."
                        )


                # =========================
                # Debug Information
                # =========================

                with st.expander(
                    "🔍 Response Details"
                ):

                    st.json(result)


            # =========================
            # API Error
            # =========================

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.code(
                    response.text
                )


        # =========================
        # Connection Error
        # =========================

        except requests.exceptions.ConnectionError:

            st.error(
                """
                ❌ Could not connect to the FastAPI backend.

                Please make sure the backend is running:

                `uvicorn backend.main:app --reload`
                """
            )


        # =========================
        # Timeout
        # =========================

        except requests.exceptions.Timeout:

            st.error(
                "⏳ The request took too long. Please try again."
            )


        # =========================
        # Unexpected Error
        # =========================

        except Exception as e:

            st.error(
                f"Unexpected error: {str(e)}"
            )

            