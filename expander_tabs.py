import streamlit as st
import random
import string

# Function to generate random text based on input
def generate_text(prompt):
    return f"Result for '{prompt}': " + ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=100))

# Initialize session state to store search history
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# UI elements
st.title("Text Search with Tabbed History")

with st.expander("Search and View Results"):
    user_input = st.text_input("Enter your text", key="text_input")
    submit_clicked = st.button("Submit")

    if submit_clicked and user_input.strip():
        result = generate_text(user_input.strip())

        # Add new result to queue (max length 3)
        st.session_state.search_history.append((user_input.strip(), result))
        if len(st.session_state.search_history) > 3:
            st.session_state.search_history.pop(0)

    if st.session_state.search_history:
        # Reverse the history for most recent first
        reversed_history = st.session_state.search_history[::-1]
        tabs = st.tabs([f"Search {i+1}" for i in range(len(reversed_history))])
        for i, (prompt, result) in enumerate(reversed_history):
            with tabs[i]:
                st.markdown(f"**Input**: {prompt}")
                st.write(result)
