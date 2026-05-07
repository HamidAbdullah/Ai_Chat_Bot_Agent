"""
Streamlit app entrypoint for the modern AI assistant UI.
"""

import streamlit as st

from brain import AssistantBrain
from config import settings
from memory import ConversationMemory
from ui.styles import get_custom_css


st.set_page_config(
    page_title=settings.app_title,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)


@st.cache_resource
def get_brain() -> AssistantBrain:
    """Create one assistant brain instance for app lifecycle."""
    return AssistantBrain()


@st.cache_resource
def get_memory() -> ConversationMemory:
    """Create one memory manager instance for app lifecycle."""
    return ConversationMemory(
        history_file=settings.history_file,
        max_memory_messages=settings.max_memory_messages,
    )


brain = get_brain()
memory = get_memory()

if "chat_id" not in st.session_state:
    st.session_state.chat_id = memory.create_new_chat()

if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "🧑"

if "ai_avatar" not in st.session_state:
    st.session_state.ai_avatar = "🤖"

with st.sidebar:
    st.markdown("## Kivyx AI Agent")
    st.caption("ChatGPT-style assistant")

    if st.button("New Chat", use_container_width=True):
        st.session_state.chat_id = memory.create_new_chat()
        st.rerun()

    if st.button("Clear Chat", use_container_width=True):
        memory.clear_chat(st.session_state.chat_id)
        st.rerun()

    st.markdown("---")
    st.markdown("### Chat History")

    all_sessions = memory.get_sessions()
    sorted_sessions = sorted(
        all_sessions.items(),
        key=lambda item: item[1].get("updated_at", ""),
        reverse=True,
    )

    for sid, session in sorted_sessions[:15]:
        title = session.get("title", "Untitled")
        if st.button(title, key=f"chat_{sid}", use_container_width=True):
            st.session_state.chat_id = sid
            st.rerun()

    st.markdown("---")
    st.markdown("### Settings")
    st.write(f"**Model:** `{settings.model_name}`")
    st.write(f"**Memory Window:** `{settings.max_memory_messages}`")

st.markdown(
    (
        '<div class="topbar">'
        '<div class="topbar-title">Kivyx AI Agent</div>'
        '<div class="topbar-subtitle">Smart, tool-enabled, memory-aware assistant</div>'
        "</div>"
    ),
    unsafe_allow_html=True,
)

messages = memory.get_messages(st.session_state.chat_id)
for m in messages:
    avatar = st.session_state.user_avatar if m["role"] == "user" else st.session_state.ai_avatar
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

prompt = st.chat_input("Type your message...")
if prompt:
    memory.add_message(st.session_state.chat_id, "user", prompt)
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=st.session_state.ai_avatar):
        with st.spinner("Kivyx AI Agent is thinking..."):
            context = memory.get_recent_context(st.session_state.chat_id)
            reply = brain.respond(context, prompt)
            st.markdown(reply)

    memory.add_message(st.session_state.chat_id, "assistant", reply)
