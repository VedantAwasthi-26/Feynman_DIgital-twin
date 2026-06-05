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
st.markdown("""
<style>

/* Sidebar */

section[data-testid="stSidebar"] {
    border-right: 2px solid #C19A6B;
}

/* Headers */

h1 {
    color: #C19A6B;
}

/* Expander */

.streamlit-expanderHeader {
    color: #C19A6B;
    font-weight: 600;
}

/* Selectboxes */

div[data-baseweb="select"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='text-align:center;color:#C19A6B;'>
    <u>Richard Feynman Digital Twin</u>
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "Learn physics through the Feynman method of explanation."
)

st.sidebar.header("🎓 Learning Settings")
teaching_style = st.sidebar.selectbox(
    "Teaching Style",
    [
        "Curious Child",
        "College Student",
        "Fellow Physicist"
    ]
)
learning_preference = st.sidebar.selectbox(
    "Learning Preference",
    [
        "Analogies",
        "Real-World Examples",
        "Visual Thinking",
        "Mathematical"
    ]
)
response_length = st.sidebar.selectbox(
    "Response Length",
    [
        "Brief",
        "Normal",
        "Detailed"
    ]
)
st.sidebar.divider()
st.sidebar.header("🧑‍🏫 Feynman Features")
show_chalkboard = st.sidebar.checkbox(
    "Show Feynman's Chalkboard"
)
st.sidebar.divider()
st.sidebar.header("💬 Conversation")
if st.sidebar.button("🗑 Clear Conversation"):
    st.session_state.chat_history = []
    st.rerun()

teaching_prompt = {
    "Curious Child":
        "Use very simple language, shorter answers, everyday analogies, and explain concepts as if teaching an intelligent 14-year-old.",

    "College Student":
        "Balance intuition and technical depth. Use examples and reasoning while keeping explanations accessible.",

    "Fellow Physicist":
        "Use rigorous reasoning, technical terminology, and deeper scientific discussion when appropriate."
}
learning_prompt = {
    "Analogies":
        "Prefer analogies and comparisons to explain ideas.",

    "Real-World Examples":
        "Use practical real-world examples whenever possible.",

    "Visual Thinking":
        "Help the user visualize concepts with mental pictures and intuitive descriptions also emphasise on the visuals.",

    "Mathematical":
        "Include and show(important parts) mathematical reasoning and formulas when useful."
}
length_prompt = {
    "Brief":
        "Keep the response concise and under 100 words when possible.",

    "Normal":
        "Provide a balanced explanation with moderate detail.",

    "Detailed":
        "Provide a thorough explanation with examples and additional context."
}
chalkboard_prompt = ""
if show_chalkboard:
    chalkboard_prompt = """
        Structure your explanation as Feynman's chalkboard notes.

        Do NOT include greetings or conversational introductions.

        Begin immediately with:

        [WHAT DO WE KNOW?]

        content

        [SIMPLE PICTURE OR ANALOGY]

        content

        [KEY IDEA]

        content

        [TAKEAWAY]

        content

        Use the square-bracket headers exactly as shown.
        Do not use markdown, stars, hashtags, underlines,
        horizontal lines, separators, or code blocks.
        """

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


if len(st.session_state.chat_history) == 0:
    if len(st.session_state.chat_history) == 0:
        st.markdown(
            """
            <div style="
            padding:10px;
            border-left:2px solid #C19A6B;
            margin-bottom:20px;
            ">
            <h5 style="color:#C19A6B;">
            Welcome
            </h5>

            Ask me about physics, mathematics, curiosity, learning, or how the world works.
            </div>
            """,
            unsafe_allow_html=True
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
        context, sources = get_context(user_input)
        st.expander("Knowledge Base Part").write(context[:600])
        try:
            response = model.generate_content(
            f"""
            {persona}

            Teaching Style:

            {teaching_prompt[teaching_style]}

            Learning Preference:

            {learning_prompt[learning_preference]}

            Response Length:

            {length_prompt[response_length]}
            
            Feynman's Chalkboard:

            {chalkboard_prompt}

            Conversation History:

            {history}

            Relevant Information From Richard Feynman's Writings:

            {context}

            User Question:
            {user_input}
            """
            )

            if show_chalkboard:
                st.markdown(
                    f"""
                    <div style="
                    background-color:#0f1a0f;
                    color:#D6C5B4;
                    padding:15px;
                    border-radius:20px;
                    border:3px solid #C19A6B;
                    font-family:Georgia;
                    ">
                    <h2 style="
                    text-align:center;
                    margin-bottom:20px;
                    color:#C19A6B;
                    ">
                    FEYNMAN'S CHALKBOARD
                    </h2>

                    {response.text.replace("\n", "<br>")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.write(response.text)
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": response.text
                }
            )
            clean_sources = []

            for source in sources:
                clean_sources.append(
                    source.replace(".txt", "")
                        .replace("_", " ")
                )

            with st.expander("Sources Used"):
                for source in clean_sources:
                    st.write(f"• {source}")
        except Exception as e:
            st.error(f"Gemini API Error: {e}")