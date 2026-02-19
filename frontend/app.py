import streamlit as st
import requests
from datetime import datetime

# Page config
st.set_page_config(page_title="SwasthyaSathi Demo", page_icon="💬", layout="centered")

# Custom CSS to fix colors
st.markdown("""
    <style>
        /* User bubble (green) */
        .user-bubble {
            background-color: #25D366; /* WhatsApp green */
            color: white;
            padding: 10px 14px;
            border-radius: 10px;
            max-width: 70%;
            display: inline-block;
            font-size: 15px;
        }
        /* Bot bubble (white) */
        .bot-bubble {
            background-color: #f1f0f0;
            color: black;
            padding: 10px 14px;
            border-radius: 10px;
            border: 1px solid #EAEAEA;
            max-width: 70%;
            display: inline-block;
            font-size: 15px;
        }
        /* Chat container */
        .chat-row {
            margin: 8px 0;
        }
        .right-align {
            text-align: right;
        }
        .left-align {
            text-align: left;
        }
        /* Timestamp */
        .timestamp {
            font-size: 10px;
            color: grey;
            margin-top: 2px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h2 style='text-align: center;'>💬 SwasthyaSathi – AI Public Health Chatbot</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Accessible via WhatsApp, SMS, and Web</p>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role, text, timestamp = msg
    if role == "user":
        st.markdown(
            f"<div class='chat-row right-align'><div class='user-bubble'>{text}</div>"
            f"<div class='timestamp'>{timestamp}</div></div>", unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-row left-align'><div class='bot-bubble'>{text}</div>"
            f"<div class='timestamp'>{timestamp}</div></div>", unsafe_allow_html=True
        )

# Divider line
st.markdown("---")

# Input field at bottom
prompt = st.chat_input("Type your message...")

if prompt:
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append(("user", prompt, timestamp))

    # Call backend
    try:
        resp = requests.post(
            "http://127.0.0.1:8000/query",  # update if running on another port
            json={"From": "demo", "Body": prompt},
            timeout=50  # 50 seconds timeout to match backend
        )
        if resp.status_code == 200:
            answer = resp.json().get("answer", "⚠️ Sorry, something went wrong.")
        else:
            answer = f"⚠️ Error: Backend returned status code {resp.status_code}"
    except requests.exceptions.Timeout:
        answer = "⚠️ Error: The request timed out. The backend might be overloaded or the API quota exceeded."
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append(("bot", answer, timestamp))

    st.rerun()
