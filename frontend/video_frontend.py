import streamlit as st
from video_backend import generate_video_for_paper, pdf_title_map
import base64
import pandas as pd

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
            background: url("data:image/jpeg;base64,{bg_base64}") no-repeat center center fixed;
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

        /* Output boxes - translucent white */
        .output-box {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 10px;
            border-radius: 5px;
        }}

        /* Logo and title container */
        .header-container {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .header-container img {{
            width: 250px;
            height: auto;
        }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Fix for Dropdown Styling (White Background, Black Text)
# --------------------------
st.markdown("""
    <style>
        /* Closed dropdown */
        div[data-baseweb="select"] > div {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: black !important;
            border: 2px solid #800000 !important;
            border-radius: 5px !important;
            width: 400px !important;
        }

        /* Open dropdown menu */
        ul[role="listbox"] {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid #800000 !important;
        }

        /* List items in dropdown */
        ul[role="listbox"] li {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: black !important;
        }

        /* Dropdown label */
        label[data-testid="stWidgetLabel"] {
            color: #800000 !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Load CSV
# --------------------------
df = pd.read_csv("paper-scope+dataset - Sheet1.csv")

# --------------------------
# Logo + Title
# --------------------------
st.markdown(f"""
<div class="header-container">
    <img src="data:image/png;base64,{logo_base64}" alt="AIM Lab Logo">
    <div>
        <h1>AIM Researcher</h1>
        <p>
        Welcome!<br>
        Select a research paper to explore:
        </p>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

# --------------------------
# Narrator Section
# --------------------------
st.title("🎙 AI Research Paper Narrator")
st.write("Select a research paper and generate a narrated video.")

# Paper selection dropdown
paper_title = st.selectbox("Choose a research paper:", list(pdf_title_map.keys()))

# Generate Video Button
if st.button("Generate Narrated Video"):
    with st.spinner("🎥 Generating narrated video... Please wait."):
        video_path, error = generate_video_for_paper(paper_title)
        if error:
            st.error(error)
        else:
            st.success("✅ Video generated successfully!")
            st.video(video_path)
