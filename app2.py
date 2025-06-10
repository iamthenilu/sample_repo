import streamlit as st
import base64

# Sample data
data = {
    "id_001": {
        "text": "This is a sample excerpt from document 1.",
        "file": R"C:\Users\User\Documents\ML Resources\Resumes\Resume_Niladri_Sen_1306.pdf"
    },
    "id_002": {
        "text": "Here is another excerpt from document 2.",
        "file": "sample2.pdf"
    },
    "id_003": {
        "text": "A third document gives us this snippet.",
        "file": "sample3.pdf"
    }
}

st.set_page_config(layout="wide")
# --- Generate Annotated Text ---
annotated_text = ""
for i, (doc_id, content) in enumerate(data.items()):
    annotated_text += f'<a href="/?doc_id={doc_id}" target="_self" style="color: blue; text-decoration: underline;">[{i+1}]</a> {content["text"]} '

# --- Read Query Parameter ---
query_params = st.experimental_get_query_params()
print(query_params)
clicked_doc_id = query_params.get("doc_id", [None])[0]

# --- Layout ---
if clicked_doc_id and clicked_doc_id in data:
    # Two-column layout: Left text + Right viewer
    left_col, right_col = st.columns([2, 3], gap="large")

    with left_col:
        st.markdown("### Annotated Text")
        st.markdown(annotated_text, unsafe_allow_html=True)

    with right_col:
        st.markdown("### Document Viewer")

        # --- Close Button ---
        if st.button("Close PDF Viewer"):
            # Clear the query parameter and rerun
            st.experimental_set_query_params()
            st.rerun()

        # --- PDF Display ---
        filename = data[clicked_doc_id]["file"]
        try:
            with open(filename, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"File '{filename}' not found.")
else:
    # Default: show only the left text
    st.markdown("### Annotated Text")
    st.markdown(annotated_text, unsafe_allow_html=True)
