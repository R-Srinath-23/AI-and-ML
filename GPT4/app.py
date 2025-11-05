import streamlit as st
from openai import AzureOpenAI
import os

# --- Azure OpenAI Configuration ---
AZURE_OPENAI_ENDPOINT = "https://kgsow-mgwfjt4s-swedencentral.cognitiveservices.azure.com/"
AZURE_OPENAI_API_KEY = "YOUR_AZURE_API_KEY_HERE"
AZURE_OPENAI_DEPLOYMENT = "gpt-4.1-2"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"

# Initialize the Azure client
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
)

# --- Streamlit UI ---
st.set_page_config(page_title="Azure GPT Chat", page_icon="💬", layout="centered")

st.title("💬 Chat with Azure OpenAI (GPT-4.1)")
st.write("Ask anything below — powered by your Azure GPT deployment.")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Input box
user_input = st.chat_input("Type your question here...")

# --- Chat Logic ---
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Call Azure OpenAI
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=st.session_state.messages,
            max_completion_tokens=500,
            temperature=0.7,
        )

    # Extract and display reply
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)
