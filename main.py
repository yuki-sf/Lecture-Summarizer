import streamlit as st
from streamlit_chat import message  # ✅ Fix: replaced st_chat_message
import pandas as pd
from datetime import datetime
from summarizer import summary_agent

st.title("AI Lecture Summarizer")
tab1, tab2 = st.tabs(["Chat", "Made By"])

if "llm_chain" not in st.session_state:
    st.session_state.llm_chain = summary_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

def append_state_messages(user_message, bot_message):
    st.session_state.messages.append({"user_message": user_message, "bot_message": bot_message})

def restore_history_messages():
    for history_message in st.session_state.messages:
        message(history_message["user_message"], is_user=True, key=str(datetime.now()))
        message(history_message["bot_message"], is_user=False, key=str(datetime.now()))

user_message = st.chat_input(placeholder="Type or paste a YouTube/Article URL...")

with tab1:
    st.header("Summarizer")
    if user_message:
        restore_history_messages()
        with st.spinner("Summarizing..."):
            output = st.session_state.llm_chain.summarize(user_message)
        message(user_message, is_user=True, key="user_message")
        message(output, is_user=False, key="bot_message")
        append_state_messages(user_message, output)

with tab2:
    st.header("Details")
    st.info("Created by: Sambhab Ranjan Mahana \n\n This is an AI Lecture Summarizer that uses Huggingface AI model to summarize YouTube videos and articles.")
