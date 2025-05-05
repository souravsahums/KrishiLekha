import os
import streamlit as st
import streamlit.components.v1 as components
import uuid
from agents.agri_agent import get_agri_agent
from utils.ocr_utils import extract_texts_from_pdf
from utils.vector_utils import get_vectore_store, add_to_vectorstore
from utils.voice_transcriber_util import transcribe_audio

from streamlit_mic_recorder import mic_recorder
from langchain.schema import HumanMessage, AIMessage

# Set Streamlit page config
st.set_page_config(
    page_title="KrishiLekha",
    page_icon="🌾",
    layout="wide"
)

# Inject custom HTML (optional) to further control the tab
components.html(
    """
    <script>
        document.title = "🌾 KrishiLekha";
    </script>
    """,
    height=0,
)
st.title("🌾 KrishiLekha")

# Generate or retrieve session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
session_id = st.session_state["session_id"]

# Initialize vector store and agent
vectorstore = get_vectore_store()
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

    # Persistent message list
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

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

    text_input = st.text_input("💬 Ask your personalized query:")
    user_query = transcript if transcript else text_input

    if user_query:
        st.session_state["chat_history"].append(HumanMessage(content=user_query))
        st.info("Running agent with tools...")
        with st.spinner("Generating answer..."):
            response = agent(user_query, session_id)
            print("Agentic response:", response)
            answer = response.get("result", "")
            chat_history = response.get("chat_history", [])
        
            if answer:
                st.session_state["chat_history"].append(AIMessage(content=answer))

            
            # Optional: Overwrite with returned chat history if it's valid
            if chat_history:
                st.session_state["chat_history"] = chat_history

     # Render chat history
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):  # LangChain Message object
            user_msg = msg.content
            user_msg = user_msg.replace("User:", "").replace("user:", "").strip()
            user_msg = user_msg.replace("Please respond in the same language as the question.", "").strip()
            st.markdown(f"**🧑 You:** {user_msg}")
        elif isinstance(msg, AIMessage):  # LangChain Message object
            st.markdown(f"**🤖 Agent:** {msg.content}")
