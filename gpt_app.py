import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai
import os
import sys
import time
from pathlib import Path
import tempfile
from dotenv import load_dotenv

# --- Load environment variables and validate API key ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Error: GOOGLE_API_KEY not found! Please set it in your environment.")
    sys.exit(1)
genai.configure(api_key=GOOGLE_API_KEY)

# --- Streamlit config ---
st.set_page_config(page_title="Video Summarizer", page_icon="📽️", layout="wide")
st.title("Video Summarizer Agent 📽️")
st.header("Powered by Gemini")

# --- Agent initialization (cached for speed) ---
@st.cache_resource
def get_agent():
    return Agent(
        name="Video Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY),
        tools=[DuckDuckGo()],
        markdown=True
    )
agent = get_agent()

def analyze_video(video_path, user_query):
    """Uploads, waits for processing, and analyzes using the multimodal agent."""
    processed_video = upload_file(video_path)
    while processed_video.state.name == "PROCESSING":
        time.sleep(1)
        processed_video = get_file(processed_video.name)
    prompt = (
        f"Analyze the uploaded video for content and context.\n"
        f"Respond to the following query using video insights and supplementary web research:\n"
        f"{user_query}\n"
        f"Provide a detailed, user-friendly, and actionable response."
    )
    return agent.run(prompt, videos=[processed_video]).content

# --- UI: File uploader and query input ---
video_file = st.file_uploader(
    "Upload a video file", type=['mp4','mov','avi'], help="AI-powered video analysis!"
)

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    st.video(video_path, format="video/mp4", width=300)
    user_query = st.text_area(
        "What insights are you seeking from this video?",
        placeholder="Ask about the content. The AI agent can use web context too."
    )

    if st.button("🔍 Analyze Video"):
        if not user_query.strip():
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    result = analyze_video(video_path, user_query)
                st.subheader("Analysis Result")
                st.markdown(result)
            except Exception as error:
                st.error(f"An error occurred: {error}")
            finally:
                Path(video_path).unlink(missing_ok=True)
else:
    st.info("Upload a video file to begin analysis.")

# --- Custom text area height (UX polish) ---
st.markdown(
    """
    <style>
    .stTextArea textarea { height: 100px; }
    </style>
    """,
    unsafe_allow_html=True
)