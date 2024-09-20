import streamlit as st
import logging
from inference_pipeline import LLMTikTok
from router import routeLayer

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize inference endpoint
inference_endpoint = LLMTikTok()

# Streamlit app
st.title("Q/A AI Agent")

st.write("""
    This is a simple Q/A AI agent. You can ask questions and get responses from the AI.
""")

query = st.text_area("Enter your query here:")

if st.button("Submit"):
    if query:
        mechanism = routeLayer.route(query).name

        response = inference_endpoint.generate(
            query=query,
            mechanism=mechanism,
            enable_rag=False,
            enable_evaluation=True,
            enable_monitoring=True,
        )

        st.write("### Answer:")
        st.write(response['answer'])

        st.write("### LLM Evaluation Result:")
        st.write(response['llm_evaluation_result'])

        # Log the response
        logger.info(f"Answer: {response['answer']}")
        logger.info("=" * 50)
        logger.info(f"LLM Evaluation Result: {response['llm_evaluation_result']}")
    else:
        st.write("Please enter a query.")