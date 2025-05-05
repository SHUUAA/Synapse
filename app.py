import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API with the newer client approach
client = genai.Client(api_key=GEMINI_API_KEY)

# Set page configuration
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="wide"
)

# App title
st.title("🤖 Synapse")
st.markdown("Chat with Gemini AI model")

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
        # Using the newer client approach
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Using the newer model you referenced
            contents=prompt
        )
        
        # Check if we have a valid response
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
    st.header("About")
    st.markdown("""
    This chatbot uses Google's Gemini AI model to generate responses to your questions.
    
    Enter your message in the chat input below and press Enter to send.
    """)
    
    # Add model selection dropdown
    st.header("Model Settings")
    model_option = st.selectbox(
        "Select Gemini Model",
        ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.0-pro"],
        index=0
    )
    
    # Update the function to use the selected model
    def update_model():
        st.session_state.selected_model = model_option
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gemini-2.0-flash"
    
    st.button("Apply Model", on_click=update_model)
    
    st.header("Chat Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
        
    st.header("Usage Tips")
    st.markdown("""
    **Free Tier Limitations:**
    - The free tier has rate limits
    - Keep questions concise for best results
    - If you hit rate limits, wait a few moments
    
    **Helpful Prompts:**
    - "Explain [topic]"
    - "Help me with [problem]"
    - "Write a [content type] about [topic]"
    """)