import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# load the environment
load_dotenv()

# configure streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini AI - Agent",
    page_icon=":robot_face:",
    layout="wide"
)

# Get the API key
API_KEY = os.getenv("GOOGLE_API_KEY")
# Models
GOOGLE_GEN_AI_MODEL = "gemini-pro"

# Setup Google API Key to Gemini AI Model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(GOOGLE_GEN_AI_MODEL)

# Initialize session chat which is already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("Chat with Google Gemini Pro...")

# Display the chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(msg['role']):
        st.markdown(["content"])


# Gemini AI response
def ai_response(user_query):
    # Use the session's model to generate a response
    resp = st.session_state.chat_session.model.generate_content(user_query)
    print(f"Gemini's Response: {resp}")
    return resp.parts[0].text


# Input the user message
user_input = st.chat_input("What is the question?")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # send user's message to Gemini and get the response
    response = ai_response(user_input)

    # Display the response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "assistant", "content": response})
