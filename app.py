import time
import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from PIL import Image

# -------------------------
# 1️⃣ Setup & Security
# -------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ API key not found. Please add GEMINI_API_KEY to your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# -------------------------
# 2️⃣ Page Layout
# -------------------------
st.set_page_config(page_title="AI Student Tutor Pro", page_icon="🎓", layout="centered")
st.title("🎓 AI Student Tutor Pro")
st.markdown("---")

# -------------------------
# 3️⃣ Session Memory
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# 4️⃣ Sidebar Tools
# -------------------------
with st.sidebar:
    st.header("📚 Study Tools")

    uploaded_file = st.file_uploader(
        "Upload Homework Photo",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("🗑 Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# -------------------------
# 5️⃣ Show Previous Messages
# -------------------------
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# 6️⃣ Chat Input
# -------------------------
if user_input := st.chat_input("Ask a question (Example: Explain gravity or solve x² + 5x + 6)"):

    # Save user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    contents = [user_input]

    # Add image if uploaded
    if uploaded_file:
        img = Image.open(uploaded_file)
        contents.append(img)
        st.image(img, caption="Analyzing your homework...", width=250)

    # -------------------------
    # 7️⃣ AI Response
    # -------------------------
    with st.spinner("🧠 Tutor is thinking..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(

                    # ⭐ Improvement: Better tutoring instructions
                    system_instruction="""
                    You are a friendly and professional AI tutor.

                    Rules:
                    - Explain answers step by step
                    - Use bullet points
                    - Use simple language
                    - Encourage the student
                    - Format math using LaTeX when needed
                    """
                )
            )

            full_response = response.text

            # ⭐ Improvement: Typing effect
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                typed_text = ""

                for word in full_response.split():
                    typed_text += word + " "
                    message_placeholder.markdown(typed_text)
                    st.sleep(0.02)

            # Save response
            st.session_state.chat_history.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:

            # ⭐ Improvement: Better error message
            st.error(f"⚠️ Connection Error: {e}")

            st.info("""
Things to check:

1️⃣ API key in `.env` file  
2️⃣ Internet connection  
3️⃣ Installed package: `google-genai`
""")
