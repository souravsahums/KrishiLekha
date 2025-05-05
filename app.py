import os

from misc.download_models import download_model
download_model()

import streamlit as st
import uuid
from agents.agri_agent import get_agri_agent
from utils.ocr_utils import extract_texts_from_pdf
from utils.vector_utils import get_vectorstore, add_to_vectorstore
from utils.voice_transcriber_util import transcribe_audio

from streamlit_mic_recorder import mic_recorder

st.set_page_config(layout="wide")
st.title("🌾 KrishiLekha")

# Generate or retrieve session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
session_id = st.session_state["session_id"]

# Initialize vector store and agent
vectorstore = get_vectorstore()
agent = get_agri_agent()

tab1, tab2 = st.tabs(["📄 Upload & Parse PDF", "🤖 Ask Personalized Questions"])

with tab1:
    st.header("Upload handwritten/scanned PDF (English or Hindi)")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_file:
        st.success("✅ PDF uploaded. Extracting text...")
        texts = extract_texts_from_pdf(uploaded_file.read())
        for t in texts:
            st.markdown(f"- {t}")

        if texts:
            st.info("Storing in Chroma vector database...")
            metadata = [{"source": uploaded_file.name}] * len(texts)
            add_to_vectorstore(vectorstore, texts, metadata)
            st.success("✅ Stored in vector database.")

with tab2:
    st.header("Ask questions using your uploaded documents + Agri web info")
    audio_file = mic_recorder(
        start_prompt="🎙️ Click to record your query",
        stop_prompt="⏹️ Stop recording",
        just_once=True,
        use_container_width=False,
        format="wav",
        key='recorder'
    )

    transcript = None

    if audio_file:
        st.audio(audio_file["bytes"], format=f"audio/{audio_file['format']}")
        audio_file_path = os.path.join(os.path.dirname(__file__), f"temp_audio.{audio_file['format']}")

        with open(audio_file_path, "wb") as f:
            f.write(audio_file["bytes"])

        # Step 1: Transcribe using Indic-ASR
        transcript = transcribe_audio(audio_file_path)
        st.success(f"📜 Transcribed: {transcript}")
        os.remove(audio_file_path) # Clean up temp file

    user_query = transcript if transcript else st.text_input("💬 Ask your personalized query:")

    if user_query:
        st.info("Running agent with tools...")
        with st.spinner("Generating answer..."):
            response = agent.invoke(
                {"input": user_query},
                config={"configurable": {"session_id": session_id}}
            )
        st.success("✅ Answer:")
        st.write(response)
