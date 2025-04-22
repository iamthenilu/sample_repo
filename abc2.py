import streamlit as st
from PIL import Image
from utils import ekb_search,ee_on_path
import os
import tempfile

# Set page configuration
st.set_page_config(page_title="Multi-Phase App", layout="wide")

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'file_content' not in st.session_state:
    st.session_state.file_content = ""
if 'extraction_json' not in st.session_state:
    st.session_state.extraction_json = {}
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Navigation function
def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()

# Handle form submission
def submit_form():
    st.session_state.form_submitted = True

# Mock function for EKB search
# def ekb_search(query):
#     # This is a static output function
#     return f"Search results for '{query}':\n- Result 1\n- Result 2\n- Result 3"

# Mock function for entity extraction from PDF
def entity_extraction_tool(pdf_path):
    # This function simulates entity extraction from a PDF
    # In a real scenario, this would use a PDF parser and extraction model
    # For this mock, we'll return dummy data based on the filename
    filename = os.path.basename(pdf_path)
    return {
        'filename': filename,
        'name': f"Person in {filename}",
        'age': '25',
        'occupation': 'Engineer',
        'location': 'New York'
    }

# Home page
def home_page():
    # Create two columns
    left_col, right_col = st.columns([1, 1])
    
    # Right column with buttons
    with right_col:
        st.title("Welcome to the Multi-Phase App")
        st.write("Choose a phase to continue:")
        if st.button("EKB Search"):
            navigate('ekb_page1')
        if st.button("Entity Extraction"):
            navigate('ee_page1')

# EKB Search Page 1
def ekb_page1():
    # Create two columns
    left_col, right_col = st.columns([1, 1])
    
    with right_col:
        st.title("EKB Search")
        query = st.text_input("Enter your search query:")
        if st.button("Submit"):
            results = ekb_search(query)
            st.write(results)
        if st.button("Home"):
            navigate('home')

# Entity Extraction Page 1
def ee_page1():
    # Create two columns
    left_col, right_col = st.columns([1, 1])
    
    # Right column for file upload
    with right_col:
        st.title("Entity Extraction")
        uploaded_files = st.file_uploader("Upload PDF files", type=['pdf'], accept_multiple_files=True)
        
        submit_button = st.button("Submit")
        if submit_button and uploaded_files:
            # Clear previous results
            st.session_state.extraction_json = []
            
            # Create a temporary directory to save the uploaded files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Process each uploaded PDF file
                for uploaded_file in uploaded_files:
                    # Save the uploaded file to the temp directory
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process the PDF file with entity extraction tool
                    extraction_result = ee_on_path(file_path)
                    
                    # Add to the list of results
                    st.session_state.extraction_json.append(extraction_result)
                    
                    # Initialize edited_values with a copy of the current extraction results
                    st.session_state.edited_values = [dict(item) for item in st.session_state.extraction_json]
            # Display all extracted entities
            st.write(f"Extracted entities from {len(uploaded_files)} PDF files:")
            for i, result in enumerate(st.session_state.extraction_json):
                st.json(result)
            
            # Trigger form display by setting a flag
            st.session_state.show_form = True
        
        if st.button("Home"):
            navigate('home')
    
    # Left column for form (only display after extraction)
    with left_col:
        if 'show_form' in st.session_state and st.session_state.show_form:
            st.title("Edit Extracted Entities")
            
            # Create tabs for each extraction result
            tabs = st.tabs([f"File {i+1}" for i in range(len(st.session_state.extraction_json))])
            
            # Make sure edited_values has the same length as extraction_json
            if len(st.session_state.edited_values) != len(st.session_state.extraction_json):
                st.session_state.edited_values = [dict(item) for item in st.session_state.extraction_json]
            
            # Create a form for each file in its respective tab
            for i, (tab, extraction) in enumerate(zip(tabs, st.session_state.extraction_json)):
                with tab:
                    with st.form(key=f"entity_form_{i}"):
                        # Exclude filename from editable fields
                        filename = extraction.get('filename', f"File {i+1}")
                        st.write(f"**Editing: {filename}**")
                        
                        for key, value in extraction.items():
                            if key != 'filename':  # Don't allow editing filename
                                st.session_state.edited_values[i][key] = st.text_input(
                                    f"{key}", 
                                    value=value, 
                                    key=f"input_{i}_{key}"
                                )
                        
                        # Submit button for each form
                        submitted = st.form_submit_button("Save Changes")
                        if submitted:
                            # Update the specific extraction result
                            st.session_state.extraction_json[i] = st.session_state.edited_values[i]
            
            # Add a separate button outside all forms to proceed to next page
            if st.button("Submit All Changes and Continue"):
                navigate('ee_page2')

# Entity Extraction Page 2
def ee_page2():
    st.session_state.show_form  = False
    # Create two columns
    left_col, right_col = st.columns([1, 1])
    
    with right_col:
        st.title("Extraction Results")
        st.write("Final Extraction JSON:")
        # Display each extraction result
        for i, result in enumerate(st.session_state.extraction_json):
            st.write(f"**File {i+1}: {result.get('filename', 'Unknown')}**")
            st.json(result)
        
        if st.button("Home"):
            navigate('home')

# Routing
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'ekb_page1':
    ekb_page1()
elif st.session_state.page == 'ee_page1':
    ee_page1()
elif st.session_state.page == 'ee_page2':
    ee_page2()