# complexity-analyser
complexity analyser for any code 


# ⏱️ Code Complexity Calculator

A streamlined web application built with **Python**, **Streamlit**, and **Google Gemini AI** that automatically calculates the Time and Space complexity ($O$ notation) of any code snippet.

## 🚀 Features
* **AI-Powered Analysis**: Uses Gemini 2.5 Flash-Lite (or 1.5 Flash) to perform deep logic analysis.
* **Support for Multiple Languages**: Analyze Python, Java, C++, JavaScript, and more.
* **Detailed Explanations**: Provides a step-by-step breakdown of *why* a specific complexity was assigned.
* **Clean UI**: Simple, intuitive interface built with Streamlit.

## 🛠️ Tech Stack
* **Frontend**: [Streamlit](https://streamlit.io/)
* **AI Engine**: [Google Gemini API](https://ai.google.dev/)
* **Language**: Python 3.9+

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/yourusername/complexity-calculator.git](https://github.com/yourusername/complexity-calculator.git)
   cd complexity-calculator
    ```
2. **Install dependencies**:
  ```bash
  pip install streamlit google-generativeai python-dotenv
  ```
3. **Set up your API Key**:
  Get a free API key from Google AI Studio.
  Create a .env file in the root directory:
  ```bash
  GEMINI_API_KEY=your_actual_key_here
  ```
(Alternatively, paste it directly into app.py for local testing).

4. 🚦 How to Run
  ```bash
  streamlit run app.py
  ```
