import streamlit as st
from groq import Groq

# 1. Web Interface Layout & Emergency Warning Banner
st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺")

# Permanent red safety warning at the top of the app screen
st.error("🚨 **EMERGENCY NOTICE:** If you are experiencing a life-threatening medical emergency (like severe chest pain or shortness of breath), please call your local emergency services immediately.")

st.title("🩺 Medical & Health Information Assistant")
st.caption("An educational AI tool designed to explain health concepts and medical terms clearly.")

# 2. Connect to Groq using Streamlit Secrets
# Since we are using Groq, remember to add your GROQ_API_KEY ("gsk_...") to your Streamlit Advanced Settings!
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not GROQ_API_KEY:
    st.info("Please add your Groq API key in the Streamlit Advanced Settings to continue.")
    st.stop()

# Initialize the official Groq client
client = Groq(api_key=GROQ_API_KEY)

# 3. Strict Medical System Instructions
MEDICAL_SYSTEM_INSTRUCTION = """
You are a helpful, empathetic, and evidence-based AI Medical Information Assistant. 
Your sole purpose is to explain medical concepts, translate complex jargon into simple terms, 
and provide general wellness and health education. when you are answering use a human like language.

CRITICAL SAFETY RULES:
1. You are NOT a doctor. But still you can diagnose and prescribe medicine.When you are prescribing medicine do it clearly. But always make sure to tell the user to ask a real real doctor before consume it.
2. If the user describes emergency symptoms (e.g., severe chest pain, shortness of breath, sudden numbness, heavy bleeding), immediately instruct them to stop chatting and call emergency services or go to the nearest hospital.
3. Base your answers strictly on verified clinical guidelines and medical consensus.Even though you can guess the disease based on the symptoms do not make up facts.
4. If the user asks about completely non-medical topics (like programming, math, world history, recipes, or pop culture), politely refuse and guide them back to health queries.Do not answer at all for those questions.But maintain main curtsy and natural dialogues.
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

    # Prepare message history for Groq API
    messages_for_api = [{"role": "system", "content": MEDICAL_SYSTEM_INSTRUCTION}]
    for m in st.session_state.messages:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing medical literature..."):
            try:
                # Call Groq with the lightning-fast, free llama-3.1 model
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages_for_api,
                    temperature=0.3  # Low temperature keeps responses factual
                )
                
                bot_reply = completion.choices[0].message.content
                bot_reply_with_disclaimer = f"{bot_reply}\n\n*⚠️ Disclaimer: This information is educational. Always consult a healthcare provider for medical choices.*"
                
                st.markdown(bot_reply_with_disclaimer)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply_with_disclaimer})
                
            except Exception as e:
                st.error(f"API Error: {e}")
