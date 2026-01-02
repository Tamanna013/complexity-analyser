import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Complexity Calculator", page_icon="⏱️", layout="centered")

# --- API SETUP ---
API_KEY = ""  # Replace with your Gemini API key or set it as an environment variable
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# --- UI DESIGN ---
st.title("⏱️ Code Complexity Calculator")
st.markdown("Paste your code below to analyze its **Time** and **Space** complexity using Gemini AI.")

code_input = st.text_area("Enter your code snippet here:", height=300, placeholder="def example_func(n):\n    for i in range(n):\n        print(i)")

if st.button("Analyze Complexity"):
    if code_input.strip() == "":
        st.warning("Please provide some code first!")
    else:
        with st.spinner("Analyzing code structure..."):
            try:
                prompt = f"""
                Analyze the following code snippet for Time and Space complexity.
                Provide the result in the following format:
                1. **Time Complexity**: (Big O notation)
                2. **Space Complexity**: (Big O notation)
                3. **Explanation**: A brief breakdown of why these complexities apply.

                Code:
                ```python
                {code_input}
                ```
                """
                
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                st.markdown("### Complexity Report")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.divider()

st.caption("Powered by Google Gemini & Streamlit")
