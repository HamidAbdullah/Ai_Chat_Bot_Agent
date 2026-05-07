"""
Custom CSS for a modern ChatGPT-style Streamlit interface.
"""


def get_custom_css() -> str:
    return """
    <style>
    :root {
        --bg: #111827;
        --surface: #1f2937;
        --surface-soft: #273244;
        --text: #eceff4;
        --muted: #aab3c5;
        --accent: #10a37f;
        --border: #334155;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .main .block-container {
        max-width: 860px;
        padding-top: 0.8rem;
        padding-bottom: 8rem;
    }

    [data-testid="stSidebar"] {
        background: #171f2d;
        border-right: 1px solid var(--border);
    }

    .topbar {
        position: sticky;
        top: 0;
        z-index: 100;
        backdrop-filter: blur(8px);
        background: rgba(17, 24, 39, 0.75);
        border-bottom: 1px solid var(--border);
        padding: 0.8rem 0;
        margin: -0.5rem 0 0.8rem 0;
    }

    .topbar-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text);
        margin: 0;
    }

    .topbar-subtitle {
        color: var(--muted);
        font-size: 0.86rem;
        margin-top: 0.2rem;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        background: var(--surface);
        padding: 0.4rem 0.45rem;
        margin-bottom: 0.45rem;
    }

    div[data-testid="stChatMessage"] p {
        line-height: 1.6;
        font-size: 0.96rem;
    }

    .stChatMessage [data-testid="stMarkdownContainer"] > p:last-child {
        margin-bottom: 0.15rem;
    }

    div[data-testid="stChatMessageAvatarUser"] + div[data-testid="stChatMessageContent"] {
        background: linear-gradient(180deg, #1f2a3d, #1b2434);
    }

    .stButton button {
        border-radius: 9px;
        border: 1px solid var(--border);
        background: var(--surface-soft);
        color: var(--text);
        height: 2.35rem;
    }

    .stButton button:hover {
        border-color: #4f9;
        transform: translateY(-1px);
    }

    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0.95rem;
        left: min(26%, 320px);
        right: 1rem;
        z-index: 999;
    }

    [data-testid="stChatInput"] > div {
        background: rgba(17, 24, 39, 0.92);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.25rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    [data-testid="stChatInput"] textarea {
        color: var(--text);
    }

    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text);
    }

    @media (max-width: 900px) {
        [data-testid="stChatInput"] {
            left: 1rem;
            right: 1rem;
        }
    }
    </style>
    """
