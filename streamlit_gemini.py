import google.generativeai as genai
import streamlit as st
import json

# Set page config with collapsed sidebar
st.set_page_config(
    page_title="ChatNow Application for Customer Operations",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar will be collapsed by default
)

# Function to initialize session state
def initialize_session_state():
    return st.session_state.setdefault('api_key', None)

# Main Streamlit app
def text_page():
    st.title("ChatNow Application for Customer Operations")

    # Initialize session state
    initialize_session_state()

    # Configure API key
    api_key = st.secrets.GEMINI_API_KEY

    # Check if the API key is provided
    if not api_key:
        st.sidebar.error("Please enter your API key.")
        st.stop()
    else:
        # Store the API key in session state
        st.session_state.api_key = api_key

    genai.configure(api_key=api_key)

    # Set up the model configuration options
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.9, 0.1)
    top_p = st.sidebar.number_input("Top P", 0.0, 1.0, 1.0, 0.1)
    top_k = st.sidebar.number_input("Top K", 1, 100, 1)
    max_output_tokens = st.sidebar.number_input("Max Output Tokens", 1, 10000, 2048)

    # Set up the model
    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
    }

    safety_settings = "{}"
    safety_settings = json.loads(safety_settings)

    # Add an instruction prompt to guide the model
    instruction_prompt = """
    You are a Customer Operations representative for a call center. Answer only questions related to previous customer interactions, customer support, and common issues reported in the call center. Provide insights and relevant data where necessary. Do not answer any questions outside of customer support topics.
    """
    
    prompt = st.text_input("Enter your Query:")
    
    # Check if the query is provided
    if not prompt:
        st.error("Please enter your query.")
        st.stop()

    # Combine the instruction with the user input
    final_prompt = f"{instruction_prompt}\nUser query: {prompt}"

    gemini = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    try:
        # Send the prompt with the instruction to the model
        response = gemini.generate_content([final_prompt])
        
        st.subheader("Gemini:")
        if response.text:
            st.write(response.text)
        else:
            st.write("No output from Gemini.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

# Run the Streamlit app
if __name__ == "__main__":
    text_page()
