from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from openai import OpenAI
from mem0 import Memory
import supabase
from supabase.client import Client, ClientOptions
import os


supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase_client = supabase.create_client(supabase_url, supabase_key)

model = os.getenv("MODEL", "gpt-4o-mini")

st.set_page_config(
    page_title="Mem0 CHat Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "logout_requested" not in st.session_state:
    st.session_state.logout_requested = False

@st.cache_resource
def get_openai_client():
    return OpenAI()

@st.cache_resource
def get_memory():
    config = {
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini"
            }
        },
        "vector_store": {
            "provider": "supabase",
            "config": {
                "connection_string": os.getenv('DATABASE_URL'),
                "collection_name": "memories"
            }
        }
    }
    return Memory.from_config(config)

client = get_openai_client()
memory = get_memory()

def signup(email, password, full_name):
    try:
        response = supabase_client.auth.sign_up({
            "email": email, 
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name
                }
            }
        })
        if response and hasattr(response, 'user'):
            st.session_state.authenticated = True
            st.session_state.user = response.user
        return response
    except Exception as e:
        st.error(f"Error signing up: {str(e)}")
        return None
    
def signin(email, password):
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": email,  
            "password": password
        })
        if response and hasattr(response, 'user'):
            st.session_state.authenticated = True
            st.session_state.user = response.user
            st.rerun()
        return response
    except Exception as e:
        st.error(f"Error signing in: {str(e)}")
        return None
    
def signout():
    try:
        supabase_client.auth.sign_out()
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.messages = []
        st.session_state.logout_requested = True
        st.rerun()
    except Exception as e:
        st.error(f"Error signing out: {str(e)}")

def chat_with_memories(message, user_id="default_user"):
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    system_assist_prompt = f"You are a helpful AI. answer the question based on query and memories \nUser Memories:\n{memories}"

    messages = [{"role": "system", "content": system_assist_prompt}, 
                {"role": "user", "content": message}]
    response = client.chat.completions.create(model=os.getenv('LLM_MODEL'), messages=messages)
    assistant_response = response.choices[0].message.content

    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response 

with st.sidebar:
    st.title("Mem0 Chat")

    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Signup"])
        
        with tab1:
            st.subheader("Login")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            login_button = st.button("Login")

            if login_button:
                if login_email and login_password:
                    signin(login_email, login_password)
                else:
                    st.warning("Please enter both email and password")

        with tab2:
            st.subheader("Signup")
            signup_email = st.text_input("Email", key="signup_email")
            signup_password = st.text_input("Password", type="password", key="signup_password")
            signup_name = st.text_input("Full Name", key="signup_name")
            signup_button = st.button("Signup")

            if signup_button:
                if signup_name and signup_email and signup_password:
                    response = signup(signup_email, signup_password, signup_name)
                    if response and hasattr(response, 'user'):
                        st.success("Signup successful! Please check your email to confirm your account")
                    else:
                        st.error("Signup failed! Please try again")
                else:
                    st.warning("Please fill in all fields")
    else:
        user = st.session_state.user
        if user:
            st.success(f"Logged in as: {user.email}")
            st.button("Logout", on_click=signout)

            st.subheader("Your Profile")
            st.write(f"User ID: {user.id}")

            st.subheader("Memory Management")
            if st.button("Clear All Memories"):
                memory.clear(user_id=user.id)
                st.success("All memories are cleared")
                st.session_state.messages = []
                st.rerun()

if st.session_state.authenticated and st.session_state.user:
    user_id = st.session_state.user.id

    st.title("Chat With Memory-Powered AI")
    st.write("Your conversation history and preferences are remembered across sessions.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
        
    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        ai_response = chat_with_memories(user_input, user_id)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.write(ai_response)
else:
    st.title("Welcome TO Mem0 Chat Assistant")
    st.write("Please login or signup to start chatting with the memory-powered AI assistant")

    st.subheader("Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🧠 Long-term Memory")
        st.write("The AI remembers your past conversations and preferences.")
    
    with col2:
        st.markdown("### 🔒 Secure Authentication")
        st.write("Your data is protected with Supabase authentication.")
    
    with col3:
        st.markdown("### 💬 Personalized Responses")
        st.write("Get responses tailored to your history and context.")