
import streamlit as st
import os
from openai import OpenAI
import google.generativeai as genai


# Configure Streamlit page and state
st.set_page_config(page_title="GemiMe", page_icon="👨‍💼")

# set default session variables
if "tweet" not in st.session_state:
    st.session_state.tweet = ""

#Rendering main page
st.title("👨‍💼 GemiMe")



with st.sidebar:
    with st.form("config"):
        st.header("Configuration")
        selection = st.radio("Select", ['debug', 'prod'])
        st.divider()
        gemini_api_key = st.text_input("Your Gemini API key", placeholder="sk-xxxx", type="password") 

        model_openai = st.selectbox(
            "OpenAI", 
            options=("gpt-3.5-turbo"),
            index=1,
        )
        model_gemini = st.selectbox(
            "Gemini",
            options=("gemini-pro", "gemini-pro-vision", "embedding-001", "embedding-gecko-001","aqa"),
            index=1,
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1, format="%.1f")
        max_retries = st.slider("Max Retries", 0, 10, 2, 1)
        if st.form_submit_button("Save"):
            if selection=='OpenAI':
                model=model_openai
            else:
                model=model_gemini
            st.session_state.model_config = {
                "gemini_api_key": gemini_api_key,
                "model": model,
                "temperature": temperature,
                "max_retries": max_retries,
            }
            st.info(f"Selected model: {model}")


tab_specs, tab_analysis, tab_design, tab_verif, tab_cost, tab_close =st.tabs(["Specifications", "Analysis", "Design", "Verification", "Costing", "Closing"])

with tab_specs:
    st.info("""Load your specification file""", icon="ℹ️")

    with st.form("Project info"):
    
        st.header("Project info")
        question=st.text_input("Enter your question:")
        submit_button = st.form_submit_button(label="Submit", disabled="model_config" not in st.session_state)

    if submit_button:
        if (st.session_state["selection"]=="prod" ): 
            genai.configure(api_key=st.session_state["gemini_api_key"])
        else:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question)
        st.success(response.text)



with tab_analysis:
    st.info("""Load your specification file""", icon="ℹ️")

