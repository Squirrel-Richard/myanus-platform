"""
MyAnus Platform - The AI That Actually Does The Work
A Manus.im-inspired autonomous AI agent platform with viral growth mechanics
"""

import streamlit as st
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import json

# Database & Auth
from supabase import create_client, Client
import psycopg_pool

# LangChain & LangGraph
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# Code Execution
try:
    from e2b_code_interpreter import CodeInterpreter
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False

# ============================================
# CONFIGURATION
# ============================================

# Page config
st.set_page_config(
    page_title="MyAnus - Autonomous AI Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", st.secrets.get("SUPABASE_URL", ""))
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", st.secrets.get("SUPABASE_ANON_KEY", ""))
SUPABASE_DB_URI = os.getenv("SUPABASE_DB_URI", st.secrets.get("SUPABASE_DB_URI", ""))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
E2B_API_KEY = os.getenv("E2B_API_KEY", st.secrets.get("E2B_API_KEY", ""))

# ============================================
# CUSTOM CSS - CYBER/DARK THEME
# ============================================

def load_custom_css():
    st.markdown("""
    <style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #151932 100%);
        color: #f9fafb;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #151932 0%, #1e2139 100%);
        border-right: 1px solid #2d3250;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f9fafb !important;
        font-weight: 700 !important;
    }
    
    h1 {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.5);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1e2139;
        border: 1px solid #2d3250;
        border-radius: 8px;
        color: #f9fafb;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 1px #6366f1;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: #1e2139;
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #6366f1 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Info Boxes */
    .stAlert {
        background: #1e2139;
        border: 1px solid #2d3250;
        border-radius: 8px;
        color: #f9fafb;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1e2139;
        border: 1px solid #2d3250;
        border-radius: 8px;
        color: #f9fafb;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        background: #0a0e27 !important;
        border: 1px solid #2d3250 !important;
        border-radius: 8px !important;
    }
    
    /* Glow Effect */
    .glow {
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 10px #6366f1, 0 0 20px #6366f1, 0 0 30px #6366f1;
        }
        to {
            text-shadow: 0 0 20px #8b5cf6, 0 0 30px #8b5cf6, 0 0 40px #8b5cf6;
        }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ============================================
# DATABASE CONNECTION
# ============================================

@st.cache_resource
def get_db_pool():
    """Create PostgreSQL connection pool"""
    if not SUPABASE_DB_URI:
        return None
    try:
        pool = psycopg_pool.ConnectionPool(
            SUPABASE_DB_URI,
            min_size=1,
            max_size=10,
            timeout=30
        )
        return pool
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

@st.cache_resource
def get_supabase_client() -> Optional[Client]:
    """Create Supabase client"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    except Exception as e:
        st.error(f"Supabase client creation failed: {e}")
        return None

# ============================================
# DATABASE FUNCTIONS
# ============================================

def get_user_profile(email: str) -> Optional[Dict]:
    """Get user profile from database"""
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        response = supabase.table("profiles").select("*").eq("email", email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error fetching profile: {e}")
        return None

def create_user_profile(email: str, full_name: str, invite_code: str) -> bool:
    """Create new user profile"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        # Validate invite code
        invite_response = supabase.table("invites").select("*").eq("code", invite_code).eq("is_valid", True).execute()
        
        if not invite_response.data or len(invite_response.data) == 0:
            st.error("Invalid or expired invite code")
            return False
        
        # Create profile
        profile_data = {
            "email": email,
            "full_name": full_name,
            "invite_code_used": invite_code,
            "credits": 1000
        }
        
        profile_response = supabase.table("profiles").insert(profile_data).execute()
        
        if profile_response.data:
            # Mark invite as used
            invite = invite_response.data[0]
            supabase.table("invites").update({
                "used_by": profile_response.data[0]["id"],
                "used_at": datetime.now().isoformat(),
                "current_uses": invite["current_uses"] + 1,
                "is_valid": False if invite["current_uses"] + 1 >= invite["max_uses"] else True
            }).eq("code", invite_code).execute()
            
            return True
        
        return False
    except Exception as e:
        st.error(f"Error creating profile: {e}")
        return False

def deduct_credits(user_id: str, amount: int, action_type: str) -> bool:
    """Deduct credits from user"""
    pool = get_db_pool()
    if not pool:
        return True  # Allow if no DB connection
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT public.deduct_credits(%s, %s, %s)",
                    (user_id, amount, action_type)
                )
                result = cur.fetchone()
                conn.commit()
                return result[0] if result else False
    except Exception as e:
        st.error(f"Error deducting credits: {e}")
        return False

def get_user_invites(user_id: str) -> List[Dict]:
    """Get user's invite codes"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table("invites").select("*").eq("created_by", user_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching invites: {e}")
        return []

# ============================================
# AGENT LOGIC
# ============================================

class AgentState(TypedDict):
    messages: list
    user_id: Optional[str]
    credits: int

def create_agent_graph():
    """Create LangGraph agent"""
    
    def agent_node(state: AgentState):
        """Main agent reasoning node"""
        messages = state["messages"]
        
        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=OPENAI_API_KEY
        )
        
        # System prompt
        system_message = SystemMessage(content="""You are MyAnus, an autonomous AI agent that actually does work.

You are not just a chatbot - you can:
- Write and execute Python code
- Create files and applications
- Search the web for information
- Analyze data and create visualizations
- Plan and execute complex multi-step workflows

When a user asks you to do something, break it down into steps and execute them.
Be proactive, helpful, and get things done.

Available tools:
- Python code execution (via E2B sandbox)
- Web search
- File creation

Always explain what you're doing and show your work.""")
        
        # Add system message if not present
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [system_message] + messages
        
        # Get response
        response = llm.invoke(messages)
        
        return {"messages": messages + [response]}
    
    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    return workflow.compile()

# ============================================
# CODE EXECUTION
# ============================================

def execute_python_code(code: str) -> Dict[str, Any]:
    """Execute Python code in E2B sandbox"""
    if not E2B_AVAILABLE or not E2B_API_KEY:
        return {
            "success": False,
            "output": "",
            "error": "E2B Code Interpreter not available. Please set E2B_API_KEY."
        }
    
    try:
        with CodeInterpreter(api_key=E2B_API_KEY) as sandbox:
            execution = sandbox.notebook.exec_cell(code)
            
            return {
                "success": not execution.error,
                "output": execution.text if execution.text else "",
                "error": execution.error.value if execution.error else None,
                "files": [f.path for f in execution.results if hasattr(f, 'path')]
            }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

# ============================================
# UI COMPONENTS
# ============================================

def render_invite_gate():
    """Render invite code entry page"""
    st.markdown("<h1 class='glow'>🤖 MyAnus</h1>", unsafe_allow_html=True)
    st.markdown("### The AI That Actually Does The Work")
    st.markdown("---")
    
    st.info("🎟️ **Invite-Only Access** - Enter your invite code to continue")
    
    with st.form("invite_form"):
        invite_code = st.text_input("Invite Code", placeholder="MYANUS-XXXXXXXX")
        email = st.text_input("Email", placeholder="you@example.com")
        full_name = st.text_input("Full Name", placeholder="John Doe")
        
        submitted = st.form_submit_button("🚀 Join MyAnus")
        
        if submitted:
            if not invite_code or not email or not full_name:
                st.error("Please fill in all fields")
            else:
                # Check if user exists
                existing_user = get_user_profile(email)
                if existing_user:
                    st.session_state.user = existing_user
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    # Create new user
                    if create_user_profile(email, full_name, invite_code):
                        st.success("Account created! Welcome to MyAnus! 🎉")
                        st.session_state.user = get_user_profile(email)
                        st.rerun()
                    else:
                        st.error("Failed to create account. Check your invite code.")

def render_sidebar():
    """Render sidebar with user info and settings"""
    with st.sidebar:
        st.markdown("## 🤖 MyAnus")
        st.markdown("*The AI That Actually Does The Work*")
        st.markdown("---")
        
        # User info
        if "user" in st.session_state and st.session_state.user:
            user = st.session_state.user
            st.markdown(f"### 👤 {user.get('full_name', 'User')}")
            st.markdown(f"**Email:** {user.get('email', 'N/A')}")
            
            # Credits
            credits = user.get('credits', 0)
            st.metric("💳 Credits", f"{credits:,}")
            
            if credits < 100:
                st.warning("⚠️ Low credits! Consider upgrading.")
            
            st.markdown("---")
            
            # Invite codes
            with st.expander("🎟️ Your Invite Codes"):
                invites = get_user_invites(user.get('id'))
                if invites:
                    for invite in invites:
                        status = "✅ Used" if not invite['is_valid'] else "🎫 Available"
                        st.code(f"{invite['code']} - {status}")
                else:
                    st.info("No invite codes yet")
            
            st.markdown("---")
            
            # Logout
            if st.button("🚪 Logout"):
                del st.session_state.user
                st.rerun()
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        # Model selection
        model = st.selectbox(
            "Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
            index=0
        )
        st.session_state.model = model
        
        # Thread ID
        thread_id = st.text_input(
            "Thread ID",
            value=st.session_state.get("thread_id", "default"),
            help="Separate conversations by project/topic"
        )
        st.session_state.thread_id = thread_id
        
        # Clear thread
        if st.button("🗑️ Clear Thread"):
            st.session_state.messages = []
            st.success("Thread cleared!")
            st.rerun()

def render_main_chat():
    """Render main chat interface"""
    st.markdown("# 💬 Chat with MyAnus")
    st.markdown("*Ask me to build something, analyze data, or execute code*")
    st.markdown("---")
    
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display messages
    for message in st.session_state.messages:
        role = message.get("role", "assistant")
        content = message.get("content", "")
        
        with st.chat_message(role):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("What would you like me to do?"):
        # Check credits
        user = st.session_state.get("user")
        if user and user.get("credits", 0) < 1:
            st.error("⚠️ Insufficient credits! Please upgrade your account.")
            return
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Simple response for now (full LangGraph integration later)
                    llm = ChatOpenAI(
                        model=st.session_state.get("model", "gpt-4o-mini"),
                        api_key=OPENAI_API_KEY
                    )
                    
                    messages = [HumanMessage(content=prompt)]
                    response = llm.invoke(messages)
                    
                    st.markdown(response.content)
                    
                    # Add to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    # Deduct credits
                    if user:
                        deduct_credits(user.get("id"), 1, "chat")
                        user["credits"] -= 1
                        st.session_state.user = user
                    
                except Exception as e:
                    st.error(f"Error: {e}")

# ============================================
# MAIN APP
# ============================================

def main():
    """Main application entry point"""
    
    # Load custom CSS
    load_custom_css()
    
    # Check if user is logged in
    if "user" not in st.session_state or not st.session_state.user:
        render_invite_gate()
    else:
        render_sidebar()
        render_main_chat()

if __name__ == "__main__":
    main()
