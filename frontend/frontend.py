import streamlit as st
from main_backend import chat_llm
from typing_extensions import TypedDict, List
import base64

# --------------------------
# Page Config - Full Width
# --------------------------
st.set_page_config(page_title="AIM Researcher", layout="wide")

# --------------------------
# Convert logo to Base64
# --------------------------
logo_path = "AIM_LAB logo.png"
with open(logo_path, "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

# --------------------------
# Convert background image to Base64
# --------------------------
bg_image_path = "download.png"
with open(bg_image_path, "rb") as f:
    bg_base64 = base64.b64encode(f.read()).decode()

# --------------------------
# Custom Styling
# --------------------------
st.markdown(f"""
    <style>
        /* Background image */
        .stApp {{
            background: url("data:image/png;base64,{bg_base64}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* Titles in maroon */
        h1, h2, h3 {{
            color: #800000 !important;
        }}

        /* Grey text */
        p, div, label {{
            color: #4B4B4B;
        }}

        /* Dropdown closed state - translucent white & shorter width */
        div[data-baseweb="select"] > div {{
            background-color: rgba(255, 255, 255, 0.8) !important;
            color: black !important;
            border: 2px solid #800000 !important;
            border-radius: 5px !important;
            width: 300px !important; /* Shorter width */
        }}

        /* Dropdown open state (menu) - opaque white & same width */
        ul[role="listbox"] {{
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: black !important;
            width: 300px !important;
        }}
        ul[role="listbox"] li {{
            color: black !important;
        }}

        /* Selectbox label */
        .stSelectbox label {{
            font-weight: bold;
            color: #800000;
        }}

        /* Divider */
        hr {{
            border: none;
            height: 2px;
            background-color: #800000;
        }}

        /* Logo and title container */
        .header-container {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .header-container img {{
            width: 200px;
            height: auto;
        }}

        /* Output boxes - translucent white */
        .output-box {{
        background-color: rgba(255, 255, 255, 0.85);
        color: black !important; /* Changed from white to black */
        padding: 10px;
        border-radius: 5px;
    }}

    </style>
""", unsafe_allow_html=True)

# --------------------------
# Header with Logo + Title
# --------------------------
st.markdown(f"""
<div class="header-container">
    <img src="data:image/png;base64,{logo_base64}" alt="AIM Lab Logo">
    <div>
        <h1>AIM Researcher</h1>
        <p>
        Welcome!<br>
        Enter your query below to explore research papers:
        </p>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

# --------------------------
# TypedDict for State
# --------------------------
class chat(TypedDict):
    user_query: str
    transformed_query: str
    metadata: List[dict]
    summaries: List[str]
    similarity_scores: List[float]
    answer: str
    token_count: int

# --------------------------
# Search Section
# --------------------------
# Shorter text input width
st.markdown("""
    <style>
        .short-input input {
            width: 1000px !important;
            background-color: rgba(255,255,255,0.8);
            border: 2px solid #800000;
            border-radius: 5px;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)
st.title("Research Paper Finder")
query = st.text_input("🔍 Your Research Query", placeholder="e.g., What is Reinforcement Learning?")
# Apply CSS class to text input
st.markdown("<style>.stTextInput {width: 1000px !important;}</style>", unsafe_allow_html=True)

if st.button("Search") and query.strip():
    with st.spinner("🔄 Processing your query..."):
        init_state: chat = {
            "user_query": query,
            "transformed_query": "",
            "metadata": [],
            "summaries": [],
            "similarity_scores": [],
            "answer": "",
            "token_count": 0
        }

        result = chat_llm.invoke(init_state)

    # Display final answer
    st.subheader("LLM Summary Answer")
    st.markdown(f"<div class='output-box'>{result['answer']}</div>", unsafe_allow_html=True)

    # Display similarity scores
    st.subheader("Similarity Scores")
    for i, score in enumerate(result["similarity_scores"], start=1):
        st.markdown(f"<div class='output-box'>Paper {i}: {round(score, 3)}</div>", unsafe_allow_html=True)

  # Display paper metadata
    st.subheader("Top 5 Research Papers")
    for i, (md, summary) in enumerate(zip(result["metadata"], result["summaries"]), start=1):
        with st.expander(f"Paper {i}: {md.get('Title', 'No Title')}"):
            st.markdown(f"""
            <div style="
                background-color: rgba(255, 255, 255, 0.85);
                padding: 15px;
                border-radius: 8px;
            ">
                <b>Title:</b> {md.get('Title', 'N/A')}<br>
                <b>Authors:</b> {md.get('Authors', 'N/A')}<br>
                <b>Published:</b> {md.get('Published', 'N/A')}<br>
                <b>URL:</b> <a href="{md.get('url', '#')}" target="_blank">{md.get('url', 'No URL')}</a><br>
                <b>Summary:</b> {summary}
            </div>
            """, unsafe_allow_html=True)


else:
    st.info("Enter a query and press **Search** to get results.")
