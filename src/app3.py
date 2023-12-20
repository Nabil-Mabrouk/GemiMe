import streamlit as st
import time
from pdfminer.high_level import extract_pages
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdfminer.high_level import extract_text
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure Streamlit page and state
st.set_page_config(page_title="GemiMe", page_icon="👨‍💼")

# Define the steps of the workflow
workflow_steps = [
    "Home",
    "Specifications",
    "Design",
    "Costing",
    "Proposal"
]

with st.sidebar:
    help='''GemiMe wil take through different steps from loading the specifications to generating a proposal. You can move from one step to another manually or let GemiMe do iy automatically'''
    st.info(help)
    with st.form("config"):
        st.header("Configuration")
        selection = st.radio("Select", ['Automatic', 'Manual'])
        gemini_api_key = st.text_input("Your Gemini API key", placeholder="sk-xxxx", type="password") 
        temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1, format="%.1f")
        max_retries = st.slider("Max Retries", 0, 10, 2, 1)

        if st.form_submit_button("Save"):
            st.session_state.model_config = {
                "selection": selection,
                "gemini_api_key": gemini_api_key,
                "temperature": temperature,
                "max_retries": max_retries,
            }
            st.success(f"Selected model: {selection}")

def load_project_specification():

    st.session_state.file_uploaded=False
    st.write("### Step 1: Loading specification file")
    # Function to upload and display the project specification
    uploaded_file = st.file_uploader("Upload Project Specification", type=["pdf", "docx"])
    if uploaded_file is not None:
        st.write("Project Specification:")
        return uploaded_file
        #st.write(uploaded_file)
        #st.session_state.file_uploaded=True
        #for page_layout in extract_pages(uploaded_file):
        #    for element in page_layout:
        #        st.write(element)
        
def main():
    #Rendering main page
    st.title("👨‍💼 GemiMe")

    tab_home, tab_specs, tab_design, tab_cost, tab_proposal =st.tabs(["Home", "Specifications", "Design", "Costing", "Proposal"])

    with tab_home:
        intro='''A proposal engineer plays a crucial role in the process of bidding for and securing projects, 
        particularly in industries where complex technical solutions are required. '''
        st.write(intro)

    with tab_specs:
        intro='''Load the specification file of the project. This file can be in pdf or docx format. You can also use one of our examples demo specifciation files below'''
        st.write(intro)
        uploaded_file=load_project_specification()
        # create llm
        #llm = OpenAI(temperature=0.7, model=st.session_state.model)
        #llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GEMINI_API_KEY"])
        #chain = load_summarize_chain(llm, chain_type="stuff")

        text = ""
        if uploaded_file is not None:
            text = extract_text(uploaded_file)

            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
        
            # Create embeddings
            #embeddings = OpenAIEmbeddings(disallowed_special=())
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=st.secrets["GEMINI_API_KEY"])
            knowledge_base = FAISS.from_texts(chunks, embeddings)

if __name__ == "__main__":
    main()