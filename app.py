import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API with the newer client approach
genai.configure(api_key=GEMINI_API_KEY)


# Set page configuration
st.set_page_config(
    page_title="Synapse AI",
    page_icon="🤖",
    layout="wide"
)

# App title
st.title("🤖 Synapse")
st.markdown("Chat with Synapse AI")

# Check if API key is valid
if not GEMINI_API_KEY:
    st.error("⚠️ No API key found. Please make sure you have created a .env file with your GEMINI_API_KEY.")
    st.stop()

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate response from Gemini using the updated API
def generate_gemini_response(prompt):
    try:
        model = genai.GenerativeModel(model_name=st.session_state.get("selected_model", "gemini-2.0-flash"))

        # Build the conversation history into the prompt.  This is key to maintaining context.
        conversation = ""
        for msg in st.session_state.messages:
            conversation += f"{msg['role']}: {msg['content']}\n"
        conversation += f"user: {prompt}\nassistant:"  # Append current user prompt

        response = model.generate_content(conversation)

        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            return "I couldn't generate a response. Please try again."

    except Exception as e:
        if "quota" in str(e).lower() or "rate" in str(e).lower() or "limit" in str(e).lower():
            return "⚠️ API rate limit reached. Please wait a moment before trying again."
        else:
            return f"An error occurred: {str(e)}"


# Get user input
user_prompt = st.chat_input("Ask something...")

if user_prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_gemini_response(user_prompt)
            st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with information
with st.sidebar:
    st.header("More Info")
    st.markdown("""
    Creating more contents soon...
    """)