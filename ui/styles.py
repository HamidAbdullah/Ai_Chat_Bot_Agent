"""
Custom CSS for a modern ChatGPT-style Streamlit interface.
"""


def get_custom_css() -> str:
    return """
    <style>
    :root {
        --bg: #0b1020;
        --card: #121a2f;
        --text: #e6ebff;
        --muted: #9ca8d4;
        --accent: #7c9cff;
        --border: #233056;
    }

    .stApp {
        background: radial-gradient(1200px 800px at 10% -20%, #1a2445 0%, var(--bg) 45%);
        color: var(--text);
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 1.2rem;
        padding-bottom: 6rem;
    }

    [data-testid="stSidebar"] {
        background: #0f1730;
        border-right: 1px solid var(--border);
    }

    .chat-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.6rem;
    }

    .muted {
        color: var(--muted);
        font-size: 0.92rem;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid var(--border);
        border-radius: 14px;
        background: rgba(18, 26, 47, 0.7);
        padding: 0.35rem 0.35rem;
    }

    .stButton button {
        border-radius: 10px;
        border: 1px solid var(--border);
        background: #182343;
        color: var(--text);
    }

    .stButton button:hover {
        border-color: var(--accent);
        color: white;
    }

    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0.9rem;
        left: min(26%, 320px);
        right: 1.2rem;
        z-index: 999;
    }

    @media (max-width: 900px) {
        [data-testid="stChatInput"] {
            left: 1rem;
            right: 1rem;
        }
    }
    </style>
    """
