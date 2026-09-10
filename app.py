import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
import streamlit as st

load_dotenv()

st.set_page_config(page_title="StudyBuddy", page_icon="📚")

st.title("📚 StudyBuddy")
st.caption("Your AI study companion powered by Gemini")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    st.error("GEMINI_API_KEY is missing. Please set it in your Streamlit Cloud Secrets (or .env locally).")
    st.stop()

client = genai.Client(api_key=api_key)

with st.sidebar:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message("user" if message.role == "user" else "assistant"):
        st.write(message.parts[0].text)

prompt = st.chat_input("Ask StudyBuddy anything...")

if prompt:
    st.session_state.messages.append(
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    )
    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=st.session_state.messages,
            )

        st.session_state.messages.append(
            types.Content(role="model", parts=[types.Part.from_text(text=response.text)])
        )
        with st.chat_message("assistant"):
            st.write(response.text)
    except APIError as e:
        st.session_state.messages.pop()
        if e.code in (400, 401, 403):
            st.error("Invalid API key or unauthorized request. Please check your GEMINI_API_KEY in .env.")
        elif e.code == 429:
            st.error("Rate limit exceeded. Please wait a moment and try again.")
        else:
            st.error(f"API Error ({e.code}): {e.message}")
