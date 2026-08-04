import streamlit as st
from google import genai
# FIXED: Updated the configuration import pathway to match the current library version
from google.genai import types

# 1. Web Interface Layout & Emergency Warning Banner
st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺")

# Permanent red safety warning at the top of the app screen
st.error("🚨 **EMERGENCY NOTICE:** If you are experiencing a life-threatening medical emergency (like severe chest pain or shortness of breath), please call your local emergency services immediately.")

st.title("🩺 Medical & Health Information Assistant")
st.caption("An educational AI tool designed to explain health concepts and medical terms clearly.")

# 2. Connect to Google GenAI using Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if not GEMINI_API_KEY:
    st.info("Please add your Gemini API key in the Streamlit Advanced Settings to continue.")
    st.stop()

# Initialize the official Google GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

# 3. Strict Medical System Instructions
MEDICAL_SYSTEM_INSTRUCTION = """
You are a helpful, empathetic, and evidence-based AI Medical Information Assistant. 
Your sole purpose is to explain medical concepts, translate complex jargon into simple terms, 
and provide general wellness and health education.

CRITICAL SAFETY RULES:
1. You are NOT a doctor. You cannot diagnose conditions, prescribe medications, or recommend treatments.
2. Every response regarding symptoms or illnesses must begin with a brief warning that this is for informational purposes only and not a substitute for professional medical advice.
3. If the user describes emergency symptoms (e.g., severe chest pain, shortness of breath, sudden numbness, heavy bleeding), immediately instruct them to stop chatting and call emergency services or go to the nearest hospital.
4. Base your answers strictly on verified clinical guidelines and medical consensus. Never guess or make up facts.
5. If the user asks about completely non-medical topics (like programming, math, world history, recipes, or pop culture), politely refuse and guide them back to health queries.
"""

# 4. Manage Chat History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous text logs on the web layout
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Inputs
if user_input := st.chat_input("Ask a medical question (e.g., Explain what a sodium test is, wellness tips)..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare message history for Gemini API
    api_messages = []
    for m in st.session_state.messages:
        # Convert Streamlit roles to Gemini format ('user' and 'model')
        role = "model" if m["role"] == "assistant" else "user"
        api_messages.append({"role": role, "parts": [{"text": m["content"]}]})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing medical literature..."):
            try:
                # Call Gemini 2.5 Flash with the safety config parameters
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=api_messages,
                    config=types.GenerateContentConfig(
                        system_instruction=MEDICAL_SYSTEM_INSTRUCTION,
                        temperature=0.3  # Low temperature keeps responses factual
                    )
                )
                
                bot_reply = response.text
                
                # Append a permanent small footnote to the bottom of the reply for safety
                bot_reply_with_disclaimer = f"{bot_reply}\n\n*⚠️ Disclaimer: This information is educational. Always consult a healthcare provider for medical choices.*"
                
                st.markdown(bot_reply_with_disclaimer)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply_with_disclaimer})
                
            except Exception as e:
                st.error(f"API Error: {e}")
3. If the user describes emergency symptoms (e.g., severe chest pain, shortness of breath, sudden numbness, heavy bleeding), immediately instruct them to stop chatting and call emergency services or go to the nearest hospital.
4. Base your answers strictly on verified clinical guidelines and medical consensus. Never guess or make up facts.
5. If the user asks about completely non-medical topics (like programming, math, world history, recipes, or pop culture), politely refuse and guide them back to health queries.
"""

# 4. Manage Chat History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous text logs on the web layout
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Inputs
if user_input := st.chat_input("Ask a medical question (e.g., Explain what a sodium test is, wellness tips)..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare message history for Gemini API
    api_messages = []
    for m in st.session_state.messages:
        # Convert Streamlit roles to Gemini format ('user' and 'model')
        role = "model" if m["role"] == "assistant" else "user"
        api_messages.append({"role": role, "parts": [{"text": m["content"]}]})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing medical literature..."):
            try:
                # Call Gemini 2.5 Flash with the safety config parameters
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=api_messages,
                    config=types.GenerateContentConfig(
                        system_instruction=MEDICAL_SYSTEM_INSTRUCTION,
                        temperature=0.3  # Low temperature keeps responses factual
                    )
                )
                
                bot_reply = response.text
                
                # Append a permanent small footnote to the bottom of the reply for safety
                bot_reply_with_disclaimer = f"{bot_reply}\n\n*⚠️ Disclaimer: This information is educational. Always consult a healthcare provider for medical choices.*"
                
                st.markdown(bot_reply_with_disclaimer)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply_with_disclaimer})
                
            except Exception as e:
                st.error(f"API Error: {e}")
4. Base your answers strictly on verified clinical guidelines and medical consensus. Never guess or make up facts.
5. If the user asks about completely non-medical topics (like programming, math, world history, recipes, or pop culture), politely refuse and guide them back to health queries.
"""

# 4. Manage Chat History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous text logs on the web layout
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Inputs
if user_input := st.chat_input("Ask a medical question (e.g., Explain what a sodium test is, wellness tips)..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare message history for Gemini API
    # Gemini requires a clean list of history messages
    api_messages = []
    for m in st.session_state.messages:
        # Convert Streamlit roles to Gemini format ('user' and 'model')
        role = "model" if m["role"] == "assistant" else "user"
        api_messages.append({"role": role, "parts": [{"text": m["content"]}]})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing medical literature..."):
            try:
                # Call Gemini 2.5 Flash with the safety config parameters
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=api_messages,
                    config=types.GenerateContentConfig(
                        system_instruction=MEDICAL_SYSTEM_INSTRUCTION,
                        temperature=0.3  # Low temperature keeps responses factual
                    )
                )
                
                bot_reply = response.text
                
                # Append a permanent small footnote to the bottom of the reply for safety
                bot_reply_with_disclaimer = f"{bot_reply}\n\n*⚠️ Disclaimer: This information is educational. Always consult a healthcare provider for medical choices.*"
                
                st.markdown(bot_reply_with_disclaimer)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply_with_disclaimer})
                
            except Exception as e:
                st.error(f"API Error: {e}")
