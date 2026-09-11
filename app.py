import streamlit as st
from auth import login
from vectorstore import load_vectorstore
from rag_pipeline import generate_answer

st.title("🏢 Enterprise HR Chatbot")

# Login
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if login(username, password):
        st.success("Login successful")
        st.session_state["logged_in"] = True
    else:
        st.error("Invalid credentials")

if st.session_state.get("logged_in"):
    query = st.text_input("Ask question:")

    if query:
        vectorstore = load_vectorstore()
        docs = vectorstore.similarity_search(query, k=3)

        context = " ".join([d.page_content for d in docs])

        response = generate_answer(context, query)

        st.write("### 🤖 Answer")
        st.write(response)