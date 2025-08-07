import streamlit as st
import requests

API_URL = "http://localhost:5000/chat"  # Flask API endpoint

st.set_page_config(page_title="Memory Powered Chatbot 💬", page_icon="🤖")
st.title("🤖 Memory Powered Chatbot")
st.markdown("Ask anything and get a response from your Memory powered agent.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history FIRST
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=False)

# Chat input at the bottom
user_input = st.chat_input("Type your message here...")

# If user sends a message
if user_input:
    # Display user message immediately
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send to API and get bot reply
    try:
        response = requests.post(API_URL, json={"message": user_input})
        response_json = response.json()
        reply = response_json.get("reply", "⚠️ Something went wrong.")
    except Exception as e:
        reply = f"❌ Failed to connect to API: {str(e)}"

    # Display bot message immediately
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
