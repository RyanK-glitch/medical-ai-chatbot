import streamlit as st
from groq import Groq
from streamlit_oauth import OAuth2Component
import json
import base64

# 1. Main Page Layout Configuration
st.set_page_config(page_title="Secure Medical AI", page_icon="🩺", layout="centered")

# Emergency Warning Banner
st.error("🚨 **EMERGENCY NOTICE:** If you are experiencing a life-threatening medical emergency, please call your local emergency services immediately.")

st.title("🩺 Medical & Health Information Assistant")
st.caption("A secure, multi-user educational assistant powered by Google Login and Groq.")

# 2. Extract Secrets Configuration Check
try:
    CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.warning("🔒 System Setup Incomplete: Make sure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GROQ_API_KEY are configured in your Streamlit Advanced Secrets.")
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

# 3. Initialize Google OAuth2 Infrastructure Components
AUTHORIZATION_URL = "https://google.com"
TOKEN_URL = "https://googleapis.com"
REVOKE_URL = "https://googleapis.com"

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_URL, TOKEN_URL, TOKEN_URL, REVOKE_URL)

# 4. Handle User Authorization Firewall Barrier
if "auth" not in st.session_state:
    st.info("👋 Welcome! Please sign in with your Google account to access the secure medical assistant panel.")
    
    # Generate the safe Google sign-in redirect button layout
    result = oauth2.authorize_button(
        name="Continue with Google",
        scope="openid email profile",
        use_container_width=True
    )
    
    if result and "token" in result:
        st.session_state.auth = result["token"]
        st.rerun()
    else:
        st.stop()

# Decode Google Identity Payload Profile Data
try:
    id_token = st.session_state.auth["id_token"]
    payload = id_token.split(".")
    # Decode baseline JWT payload layers securely
    decoded_payload = base64.urlsafe_b64decode(payload[1] + "==" * (4 - len(payload[1]) % 4)).decode("utf-8")
    user_profile = json.loads(decoded_payload)
    user_email = user_profile.get("email", "unknown_user")
    user_name = user_profile.get("name", "User")
except Exception:
    user_email = "authenticated_session"
    user_name = "User"

# 5. Active Authorized Dashboard Workspace Layout
st.sidebar.markdown(f"👤 **Account:** {user_name}")
st.sidebar.caption(f"Email: {user_email}")
if st.sidebar.button("Log Out", use_container_width=True):
    del st.session_state.auth
    st.rerun()

# 6. Manage Chat History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat logs on the screen interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Handle Active User Content Message Input Submissions
if user_input := st.chat_input("Ask an educational medical question..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare historical context matrix for the API
    messages_for_api = [{"role": "system", "content": MEDICAL_SYSTEM_INSTRUCTION}]
    for m in st.session_state.messages:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Reviewing clinical literature logs..."):
            try:
                # Call Groq API with the flagship 70B model for high medical accuracy
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api,
                    temperature=0.3
                )
                
                bot_reply = completion.choices[0].message.content
                bot_reply_with_disclaimer = f"{bot_reply}\n\n*⚠️ Disclaimer: This automated assistance structure is strictly educational. Always contact your local primary provider for professional guidance.*"
                
                st.markdown(bot_reply_with_disclaimer)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply_with_disclaimer})
                
            except Exception as e:
                st.error(f"Server Connection Issue: {e}")
