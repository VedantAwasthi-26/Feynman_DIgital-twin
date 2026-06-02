import streamlit as st
import google.generativeai as genai
import os
from rag import get_context
import chromadb

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def load_persona():
    with open("persona.md", "r", encoding="utf-8") as file:
        return file.read()


from dotenv import dotenv_values

config = dotenv_values(".env")

key = config["GEMINI_API_KEY"]
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash")


persona = load_persona()


st.set_page_config(page_title="Richard Feynman Digital Twin")

st.title("Richard Feynman Digital Twin")

st.markdown(
    "Ask Richard Feynman about physics, curiosity, learning, or science."
)

user_input = st.chat_input("Ask Feynman something...")
if user_input:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    history = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in st.session_state.chat_history[-6:]
        ]
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        context = get_context(user_input)
        st.expander("Knowledge Base Part").write(context[:600])
        try:
            response = model.generate_content(
            f"""
            {persona}

            Conversation History:

            {history}

            Relevant Information From Richard Feynman's Writings:

            {context}

            User Question:
            {user_input}
            """
            )
            st.write(response.text)
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": response.text
                }
            )
        except Exception as e:
            st.error(f"Gemini API Error: {e}")