import os
import streamlit as st
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY") or os.getenv("Groq_API_Key")
if not groq_api_key:
    raise RuntimeError("Set GROQ_API_KEY in the environment or .env file.")

client = Groq(api_key=groq_api_key)
def analyze_product(product_name):
    """Single agent: one Groq call that returns a full product-analysis report."""

    current_date = datetime.now().strftime("%b %Y")

    system_prompt = (
        "You are a senior product and business analyst. You write clear, practical, "
        "well-structured product analysis reports for founders and business teams."
    )

    user_prompt = f"""
Write a detailed product analysis report for: {product_name}.
Current month is {current_date}.
Cover the following in one flowing, well-organized report (use markdown headings and bullet points where helpful):

- Market demand and the ideal customer profile
- Marketing strategies to reach the widest possible audience (at least 5 points)
- Technology and manufacturing feasibility / key requirements (at least 5 points)
- Business model: scalability and revenue streams (at least 5 points)
- A concise Business Plan, Goals, and a launch Timeline

Keep it insightful and actionable.
"""

    response = client.chat.completions.create(
        model="groq/compound-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


def main():
    st.title("Product Analysis Dashboard")

    st.markdown(
        """
        <style>
        .reportview-container { max-width: 1200px; padding-top: 2rem; }
        h3 { color: #1f77b4; margin-top: 1rem; }
        .stExpander { border: 1px solid #f0f2f6; border-radius: 4px; margin-bottom: 1rem; }
        .stMarkdown { line-height: 1.6; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    product_name = st.text_input("Enter the product name you want to analyze:", "")

    if st.button("Analyze Product"):
        if not product_name:
            st.error("Please enter a product name before starting the analysis.")
        else:
            loading_placeholder = st.empty()
            loading_placeholder.info(f"Starting analysis for '{product_name}'... Please wait.")

            try:
                with st.spinner("Analyzing product... This may take a few moments."):
                    report = analyze_product(product_name)

                loading_placeholder.empty()
                st.subheader("Analysis Results")

                with st.expander(f"Report: {product_name}", expanded=True):
                    st.markdown(report)

            except Exception as e:
                loading_placeholder.empty()
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()