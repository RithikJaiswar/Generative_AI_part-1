import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# ---------------- PAGE ----------------

st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("🎯 Learning Mode")

mode_choice = st.sidebar.radio(
    "Choose your learning path",
    [
        "Data Science",
        "Full Stack Java",
        "Ethical Hacking"
    ]
)

if mode_choice == "Data Science":
    mode = (
        "You are a Data Science AI. "
        "Help teach, explain, and clear concepts."
    )

elif mode_choice == "Full Stack Java":
    mode = (
        "You are a Full Stack Java AI. "
        "Help teach, explain, and clear concepts."
    )

else:
    mode = (
        "You are an Ethical Hacking AI. "
        "Help teach, explain, and clear concepts."
    )

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- MODEL ----------------

model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.5,
    api_key=st.secrets['MISTRAL_API_KEY']
)

# ---------------- SESSION ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HEADER ----------------

st.title("🤖 AI Learning Assistant")

st.caption(
    f"Current Mode: {mode_choice}"
)

# ---------------- DISPLAY CHAT ----------------

for msg in st.session_state.messages:

    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])

    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ---------------- INPUT ----------------

user_prompt = st.chat_input(
    "Ask anything..."
)

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    history = [
        SystemMessage(content=mode)
    ]

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            history.append(
                HumanMessage(content=msg["content"])
            )

        else:
            history.append(
                AIMessage(content=msg["content"])
            )

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = model.invoke(history)

            st.markdown(response.content)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.content
        }
    )
