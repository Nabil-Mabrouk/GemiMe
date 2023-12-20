import streamlit as st
import time

# Define the steps of the workflow
workflow_steps = [
    "Home",
    "Load Project Specification",
    "Analysis",
    "Design",
    "Check Step",
    "Costing Process",
    "Compile Document"
]

def load_project_specification():
    time.sleep(3)
    st.session_state.file_uploaded=False
    st.write("### Step 1: Loading specification file")
    # Function to upload and display the project specification
    uploaded_file = st.file_uploader("Upload Project Specification", type=["pdf", "docx"])
    if uploaded_file is not None:
        st.write("Project Specification:")
        st.write(uploaded_file)
        st.session_state.file_uploaded=True

def analysis_step():
    time.sleep(3)
    # Function for the analysis step
    st.write("### Step 2: Analysis")
    st.info('The aim of the step is to extract from the client documents the usefull informations')
    # Add relevant analysis components and information

def design_step():
    time.sleep(3)
    # Function for the design step
    st.write("### Step 3: Design")
    # Add design components and information

def check_step():
    time.sleep(3)
    # Function for the check step
    st.write("### Step 4: Check Step")
    # Add check step components and information

def costing_process():
    time.sleep(3)
    # Function for the costing process
    st.write("### Step 5: Costing Process")
    # Add costing process components and information

def compile_document():
    time.sleep(3)
    # Function to compile the technical and commercial proposal document
    st.write("### Step 6: Compile Document")
    # Add components to compile the document

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def main():
    st.title("GemiMe")

    # Radio button for choosing between automatic and manual progression
    
    st.session_state["mode"] =None
    with st.sidebar:
        st.header("Configuration")
        progression_mode = st.radio("Progression Mode", ["Automatic", "Manual"])
        with st.form("config"):
            if st.form_submit_button("Start"):
                st.session_state["mode"] =progression_mode
                st.info(f"Selected mode: {progression_mode}")
            
            

    st.write("### AI Proposal Engineer App")
    markdown_content=read_markdown_file("ressources/home.md")
    st.markdown(markdown_content)

    # If in "Automatic" mode, progress through steps automatically
    if st.session_state["mode"]== "Automatic":
        # Create a sidebar radio button for step selection
        #current_step_index = st.sidebar.radio("Select Step", list(range(len(workflow_steps))), index=0, key="automatic_radio")
        current_step_index = st.sidebar.empty()
    
        for i, current_step in enumerate(workflow_steps):

            # Update the selected step in the sidebar
            current_step_index.radio("Select Step", workflow_steps, index=i, key=f"automatic_radio{i}", disabled=True, help="Disabled in Automatic mode")

            # Display step information based on the current step
            if current_step == "Home":
                st.divider()
            if current_step == "Load Project Specification":
                load_project_specification()
                if st.session_state.file_uploaded is not True:
                    st.empty()
                    st.write("Waiting for file upload in Step 1...")
                    st.empty()
                    continue  # Skip to the next iteration without moving to the next step

            elif current_step == "Analysis":
                analysis_step()
            elif current_step == "Design":
                design_step()
            elif current_step == "Check Step":
                check_step()
            elif current_step == "Costing Process":
                costing_process()
            elif current_step == "Compile Document":
                compile_document()

            # Add a short delay for visibility
            st.empty()
            st.write("Moving to the next step...")
            st.empty()

    # If in "Manual" mode, allow the user to select one step at a time using radio buttons
    elif st.session_state["mode"] ==  "Manual":
        selected_step = st.sidebar.radio("Select Step", workflow_steps)

        # Display step information based on the selected step
        if selected_step == "Home":
            st.divider()

        elif selected_step == "Load Project Specification":
            load_project_specification()

        elif selected_step == "Analysis":
            analysis_step()

        elif selected_step == "Design":
            design_step()

        elif selected_step == "Check Step":
            check_step()

        elif selected_step == "Costing Process":
            costing_process()

        elif selected_step == "Compile Document":
            compile_document()
    else:
        st.warning("Click start in the side bar")

if __name__ == "__main__":
    main()






