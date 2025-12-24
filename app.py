import streamlit as st
import requests
from datetime import datetime
import re

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="YouTube RAG Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# CONFIG
# =============================
API_BASE_URL = "http://localhost:8000"
ASK_ENDPOINT = f"{API_BASE_URL}/ask"

# =============================
# BEAUTIFUL CHAT UI CSS
# =============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1d2e 100%);
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d2e 0%, #0f1419 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    
    /* Sidebar brand */
    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 1rem 2rem;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .brand-logo {
        font-size: 3.5rem;
        margin-bottom: 0.75rem;
        display: block;
        filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.6));
    }
    
    .brand-title {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    .brand-tagline {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Video preview card */
    .video-preview-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 14px;
        padding: 1rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .video-preview-card:hover {
        border-color: rgba(139, 92, 246, 0.5);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.2);
        transform: translateY(-2px);
    }
    
    .video-thumbnail {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    
    .video-id-container {
        background: rgba(139, 92, 246, 0.15);
        padding: 0.75rem;
        border-radius: 8px;
    }
    
    .video-id-label {
        font-size: 0.7rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    
    .video-id-text {
        font-family: 'Courier New', monospace;
        font-size: 0.82rem;
        color: #c084fc;
        word-break: break-all;
        font-weight: 600;
    }
    
    /* Stats section */
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin: 1.5rem 0;
    }
    
    .stat-card {
        background: rgba(139, 92, 246, 0.1);
        border: 1.5px solid rgba(139, 92, 246, 0.25);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        background: rgba(139, 92, 246, 0.15);
        transform: scale(1.05);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Input fields */
    .stTextInput label {
        color: #cbd5e0 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        color: #e5e7eb !important;
        font-size: 0.9rem !important;
        padding: 0.85rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15) !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6) !important;
    }
    
    .stButton button:active {
        transform: translateY(0) !important;
    }
    
    /* Chat messages styling */
    .stChatMessage {
        background: transparent !important;
        padding: 1rem 0 !important;
    }
    
    /* User message */
    [data-testid="stChatMessageContent"]:has(div[data-testid="stMarkdownContainer"]) {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%) !important;
        border: 1.5px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 18px !important;
        padding: 1.25rem 1.5rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Assistant message */
    .stChatMessage:not(:has([aria-label="user"])) [data-testid="stChatMessageContent"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1.5px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 18px !important;
        padding: 1.25rem 1.5rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Message text */
    .stChatMessage p {
        color: #e5e7eb !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    
    /* Chat input */
    .stChatInput {
        border: none !important;
        background: transparent !important;
    }
    
    .stChatInput > div {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(30, 41, 59, 0.6) 100%) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stChatInput textarea {
        color: #e5e7eb !important;
        font-size: 0.95rem !important;
        background: transparent !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #64748b !important;
    }
    
    /* Chat input button */
    .stChatInput button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Avatar styling */
    .stChatMessage [data-testid="chatAvatarIcon-user"],
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important;
        font-size: 1.5rem !important;
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Empty state */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        text-align: center;
        padding: 2rem;
    }
    
    .empty-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        opacity: 0.6;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    .empty-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.75rem;
    }
    
    .empty-desc {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 500px;
        line-height: 1.6;
    }
    
    /* Divider */
    hr {
        border: none !important;
        border-top: 1px solid rgba(139, 92, 246, 0.2) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Alerts */
    .stAlert {
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 12px !important;
        border: 1.5px solid rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
    }
</style>
""", unsafe_allow_html=True)

# =============================
# HELPER FUNCTIONS
# =============================
def extract_video_id(url):
    if not url:
        return None
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_thumbnail_url(video_id):
    return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"

def call_api(video_id, question):
    try:
        payload = {"video_url": video_id, "question": question}
        response = requests.post(ASK_ENDPOINT, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API Error: {str(e)}")

# =============================
# SESSION STATE
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_video_id" not in st.session_state:
    st.session_state.current_video_id = None

# =============================
# SIDEBAR
# =============================
with st.sidebar:
    # Brand header
    st.markdown("""
    <div class="sidebar-brand">
        <span class="brand-logo">🎬</span>
        <div class="brand-title">YouTube RAG</div>
        <div class="brand-tagline">AI-Powered Video Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Video input
    video_url = st.text_input(
        "📺 Video URL or ID",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste a YouTube video URL or 11-character video ID"
    )
    
    # Process video URL
    if video_url:
        video_id = extract_video_id(video_url)
        if video_id:
            st.session_state.current_video_id = video_id
            
            # Show video preview
            st.markdown(f"""
            <div class="video-preview-card">
                <img src="{get_thumbnail_url(video_id)}" class="video-thumbnail" alt="Video">
                <div class="video-id-container">
                    <div class="video-id-label">Video ID</div>
                    <div class="video-id-text">{video_id}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Invalid YouTube URL or ID")
            st.session_state.current_video_id = None
    
    # Statistics
    st.markdown("---")
    
    total_messages = len(st.session_state.messages)
    questions = len([m for m in st.session_state.messages if m["role"] == "user"])
    
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{total_messages}</div>
            <div class="stat-label">Messages</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{questions}</div>
            <div class="stat-label">Questions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Actions
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_video_id = None
            st.rerun()

# =============================
# MAIN CHAT AREA
# =============================

# Display empty state or messages
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎯</div>
        <div class="empty-title">Start a Conversation</div>
        <div class="empty-desc">Enter a YouTube video in the sidebar and ask your first question below</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display all messages using Streamlit's chat message
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

# Chat input at the bottom
user_input = st.chat_input("Type your message here...", key="chat_input")

# =============================
# HANDLE USER INPUT
# =============================
if user_input:
    if not st.session_state.current_video_id:
        st.error("⚠️ Please add a YouTube video in the sidebar first")
    else:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        # Call API and get response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                try:
                    result = call_api(st.session_state.current_video_id, user_input)
                    answer = result.get("answer", "Sorry, I couldn't generate an answer.")
                    
                    # Display assistant message
                    st.markdown(answer)
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                except Exception as e:
                    error_msg = f"❌ {str(e)}"
                    st.error(error_msg)