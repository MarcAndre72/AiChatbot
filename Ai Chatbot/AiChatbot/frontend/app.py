import streamlit as st
import requests
import json
from typing import Iterator

def stream_response(response):
    """Stream response from the API"""
    for chunk in response.iter_lines():
        if chunk:
            # Skip SSE data prefix
            if chunk.startswith(b'data: '):
                chunk = chunk[6:]
            try:
                chunk_data = json.loads(chunk.decode())
                if chunk_data.get("type") == "tool_call":
                    with st.sidebar:
                        st.write("Tool Call:")
                        st.json(chunk_data["content"])
                else:
                    yield chunk_data.get("content", "")
            except json.JSONDecodeError:
                # Skip malformed chunks
                continue

st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("AI Assistant with Tool Calling")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response from the API
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": prompt},
                stream=True
            )
            response.raise_for_status()
            
            for chunk in stream_response(response):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except requests.RequestException as e:
            error_msg = str(e)
            if "Connection refused" in error_msg:
                st.error("Cannot connect to the backend server. Please ensure it's running.")
            else:
                st.error(f"Error communicating with the AI: {error_msg}")
            st.info("Try asking another question or refreshing the page.")
            
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar for tool calls
with st.sidebar:
    st.header("Tool Calls")
    st.info("Tool calls will appear here during the conversation.")
    
    
