import streamlit as st
from groq import Groq

# 1. Main Page Layout Configuration
st.set_page_config(page_title="Secure Medical AI", page_icon="🩺", layout="centered")

# Emergency Warning Banner
st.error("🚨 **EMERGENCY NOTICE:** If you are experiencing a life-threatening medical emergency, please call your local emergency services immediately.")

st.title("🩺 Medical & Health Information Assistant")
st.caption("A secure, multi-user educational assistant powered by Google Login and Groq.")

# 2. Extract Secrets Configuration Check
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.warning("🔒 System Setup Incomplete: Make sure GROQ_API_KEY is configured in your Streamlit Advanced Secrets.")
    st.stop()

# Initialize the Groq core client
client = Groq(api_key=GROQ_API_KEY)

# Strict Medical System Instructions
MEDICAL_SYSTEM_INSTRUCTION = """
You are a helpful, empathetic, and evidence-based AI Medical Information Assistant. 
Your sole purpose is to explain medical concepts, translate complex jargon into simple terms, 
and provide general wellness and health education.

CRITICAL SAFETY RULES:
1. You are NOT a doctor. You cannot diagnose conditions, prescribe medications, or recommend treatments.
2. Every response regarding symptoms or illnesses must begin with a brief warning that this is for informational purposes only and not a substitute for professional medical advice.
3. If the user describes emergency symptoms (e.g., severe chest pain, shortness of breath, sudden numbness, heavy bleeding), immediately instruct them to stop chatting and call emergency services or go to the nearest hospital.
4. Base your answers strictly on verified clinical guidelines and medical consensus. Never guess or make up facts.
5. If the user asks about completely non-medical topics, politely refuse and guide them back to health queries.
"""

# 3. Handle User Authorization Firewall Using Native Streamlit Auth
if not st.experimental_user.is_logged_in:
    st.info("👋 Welcome! Please sign in with your Google account to access the secure medical assistant panel.")
    
    # Native login engine - completely bypasses the broken popups
    if st.button("Continue with Google", use_container_width=True, type="primary"):
        st.login("google")
    st.stop()

# Get User Profile details natively from the login token
user_name = st.experimental_user.get("name", "User")
user_email = st.experimental_user.get("email", "unknown_user")

# 4. Active Authorized Dashboard Workspace Layout
st.sidebar.markdown(f"👤 **Account:** {user_name}")
st.sidebar.caption(f"Email: {user_email}")
if st.sidebar.button("Log Out", use_container_width=True):
    st.logout()
    st.rerun()

# 5. Manage Chat History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat logs on the screen interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Handle Active User Content Message Input Submissions
if user_input := st.chat_input("Ask an educational medical question..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    messages_for_api = [{"role": "system", "content": MEDICAL_SYSTEM_INSTRUCTION}]
    for m in st.session_state.messages:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Reviewing clinical literature logs..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api,
                    temperature=0.3
                )
                
                bot_reply = completion.choices.message.content
                bot_reply_with_disclaimer = f"{bot_reply}\n\n*⚠️ Disclaimer: This automated assistance structure is strictly educational. Always contact your local primary provider for professional guidance.*"
                
                st.markdown(bot_reply_with_disclaimer)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply_with_disclaimer})
                
            except Exception as e:
                st.error(f"Server Connection Issue: {e}")
