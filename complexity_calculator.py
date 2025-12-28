import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Code Complexity Calculator",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 1.5rem;
    }
    .complexity-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    .time-complexity {
        border-left-color: #10B981;
        background-color: #ECFDF5;
    }
    .space-complexity {
        border-left-color: #3B82F6;
        background-color: #EFF6FF;
    }
    .code-block {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
    .explanation-box {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #F59E0B;
    }
    .warning {
        color: #DC2626;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""

# Header
st.markdown('<h1 class="main-header">⏱️ Code Complexity Calculator</h1>', unsafe_allow_html=True)
st.markdown("Analyze time and space complexity of your code using Gemini AI")

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key_method = st.radio(
        "API Key Source",
        ["Use my own key", "Use environment variable"]
    )
    
    if api_key_method == "Use my own key":
        api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
        if api_key:
            st.session_state.gemini_api_key = api_key
    else:
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key:
            st.session_state.gemini_api_key = env_key
            st.success("✅ Using API key from environment variable")
        else:
            st.warning("⚠️ GEMINI_API_KEY not found in .env file")
    
    st.divider()
    
    # Model selection
    st.subheader("Model Settings")
    model_name = st.selectbox(
        "Select Gemini Model",
        ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
        index=0
    )
    
    # Language selection
    language = st.selectbox(
        "Programming Language",
        ["Python", "Java", "C++", "JavaScript", "C", "Go", "Rust", "Other"],
        index=0
    )
    
    st.divider()
    
    # Instructions
    st.subheader("📝 Instructions")
    st.markdown("""
    1. Enter your code in the main text area
    2. Select the programming language
    3. Click 'Analyze Complexity'
    4. View detailed analysis
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h3 class="sub-header">📝 Enter Your Code</h3>', unsafe_allow_html=True)
    
    # Code input
    default_code = """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1"""

    code_input = st.text_area(
        "Paste your code here:",
        value=default_code,
        height=300,
        placeholder="Paste your code here...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<h3 class="sub-header">⚡ Quick Tips</h3>', unsafe_allow_html=True)
    st.info("""
    **For accurate analysis:**
    - Include complete functions
    - Add comments for complex logic
    - Specify input sizes if known
    - Include helper functions
    """)
    
    st.markdown("""
    **Common Complexities:**
    - O(1) - Constant
    - O(n) - Linear
    - O(n²) - Quadratic
    - O(log n) - Logarithmic
    - O(n log n) - Linearithmic
    """)

# Analyze button
if st.button("🔍 Analyze Complexity", type="primary", use_container_width=True):
    if not code_input.strip():
        st.error("Please enter some code to analyze!")
        st.stop()
    
    if not st.session_state.gemini_api_key:
        st.error("Please configure your Gemini API key in the sidebar!")
        st.stop()
    
    # Configure Gemini
    try:
        genai.configure(api_key=st.session_state.gemini_api_key)
        model = genai.GenerativeModel(model_name)
        
        with st.spinner("Analyzing code complexity..."):
            # Prepare prompt
            prompt = f"""Analyze the following {language} code and provide a detailed complexity analysis.

Code:
{code_input}

Please analyze and provide the response in this EXACT format:

TIME COMPLEXITY: [Big O notation here, e.g., O(n), O(log n), etc.]
TIME EXPLANATION: [Detailed explanation of time complexity]

SPACE COMPLEXITY: [Big O notation here]
SPACE EXPLANATION: [Detailed explanation of space complexity]

BREAKDOWN:
[Detailed breakdown of each operation's complexity]

OPTIMIZATION SUGGESTIONS:
[Suggestions for improving time/space complexity if applicable]

EDGE CASES:
[Important edge cases to consider]

Make sure to:
1. Use proper Big O notation
2. Consider worst-case scenario
3. Account for all loops, recursions, and data structures
4. Include auxiliary space usage"""
            
            # Get response from Gemini
            response = model.generate_content(prompt)
            
            # Parse the response
            response_text = response.text
            
            # Extract information using regex
            time_match = re.search(r'TIME COMPLEXITY:\s*(.+)', response_text)
            time_exp_match = re.search(r'TIME EXPLANATION:\s*(.+)', response_text)
            space_match = re.search(r'SPACE COMPLEXITY:\s*(.+)', response_text)
            space_exp_match = re.search(r'SPACE EXPLANATION:\s*(.+)', response_text)
            breakdown_match = re.search(r'BREAKDOWN:\s*(.+?)(?=OPTIMIZATION|EDGE CASES|$)', response_text, re.DOTALL)
            optimization_match = re.search(r'OPTIMIZATION SUGGESTIONS:\s*(.+?)(?=EDGE CASES|$)', response_text, re.DOTALL)
            edge_cases_match = re.search(r'EDGE CASES:\s*(.+)', response_text, re.DOTALL)
            
            # Display results
            st.markdown("---")
            st.markdown('<h2 class="sub-header">📊 Analysis Results</h2>', unsafe_allow_html=True)
            
            # Display code
            st.markdown('<h4>📝 Your Code:</h4>', unsafe_allow_html=True)
            st.code(code_input, language=language.lower())
            
            # Time Complexity
            if time_match:
                time_comp = time_match.group(1).strip()
                st.markdown('<div class="complexity-box time-complexity">', unsafe_allow_html=True)
                st.markdown(f'**⏱️ Time Complexity:** `{time_comp}`')
                if time_exp_match:
                    st.markdown(f'**Explanation:** {time_exp_match.group(1).strip()}')
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Space Complexity
            if space_match:
                space_comp = space_match.group(1).strip()
                st.markdown('<div class="complexity-box space-complexity">', unsafe_allow_html=True)
                st.markdown(f'**💾 Space Complexity:** `{space_comp}`')
                if space_exp_match:
                    st.markdown(f'**Explanation:** {space_exp_match.group(1).strip()}')
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Detailed breakdown
            if breakdown_match:
                st.markdown('<div class="explanation-box">', unsafe_allow_html=True)
                st.markdown('**📈 Detailed Breakdown:**')
                st.markdown(breakdown_match.group(1).strip())
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Optimization suggestions
            if optimization_match:
                with st.expander("🛠️ Optimization Suggestions"):
                    st.markdown(optimization_match.group(1).strip())
            
            # Edge cases
            if edge_cases_match:
                with st.expander("⚠️ Edge Cases to Consider"):
                    st.markdown(edge_cases_match.group(1).strip())
            
            # Store in history
            analysis_entry = {
                'code': code_input[:100] + "..." if len(code_input) > 100 else code_input,
                'time_complexity': time_comp if time_match else "N/A",
                'space_complexity': space_comp if space_match else "N/A",
                'language': language
            }
            st.session_state.analysis_history.append(analysis_entry)
            
            # Show raw response in expander
            with st.expander("View Raw AI Response"):
                st.text(response_text)
                
    except Exception as e:
        st.error(f"Error analyzing code: {str(e)}")

# Display analysis history in sidebar
if st.session_state.analysis_history:
    st.sidebar.divider()
    st.sidebar.subheader("📚 Analysis History")
    
    for i, entry in enumerate(reversed(st.session_state.analysis_history[-5:]), 1):
        st.sidebar.markdown(f"""
        **Analysis {i}**
        - Language: {entry['language']}
        - Time: `{entry['time_complexity']}`
        - Space: `{entry['space_complexity']}`
        """)
        st.sidebar.code(entry['code'], language=entry['language'].lower())
        st.sidebar.divider()

# Clear history button
if st.session_state.analysis_history:
    if st.sidebar.button("Clear History"):
        st.session_state.analysis_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>Powered by Gemini AI • Built with Streamlit</p>
    <p>Note: Complexity analysis is AI-generated and should be verified</p>
</div>
""", unsafe_allow_html=True)