import streamlit as st
from backend.parser import extract_text
from backend import qa_engine, challenge_engine
from backend.summarizer import generate_summary

st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        /* Gradient background */
        body {
            background: linear-gradient(135deg, #f0f4ff, #eafaf1);
        }

        /* Glassmorphic chat box */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.65);
            border-radius: 12px;
            padding: 10px 16px;
            margin-bottom: 10px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
            backdrop-filter: blur(12px);
        }

        .stTextInput > label {
            font-weight: 600;
            color: #333;
        }

        .block-container {
            padding-top: 2rem;
        }

        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- Session Memory ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar ---
with st.sidebar:
    st.title("💬AI Research Companion")
    mode = st.radio("Mode", ["📄 Summarize + Ask", "🧩 Challenge Me"])
    st.markdown("---")
    uploaded_file = st.file_uploader("📤 Upload a PDF or TXT file", type=["pdf", "txt"])
    if st.button("🔁 Reset Conversation"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main Logic ---
if uploaded_file:
    st.success(f"🎉 File uploaded: `{uploaded_file.name}`")

    with st.spinner("🔎 Parsing document..."):
        text = extract_text(uploaded_file)

    if not text.strip():
        st.error("❌ The document is empty or unreadable.")
    else:
        if mode == "📄 Summarize + Ask":
            with st.spinner("🧠 Generating summary..."):
                summary = generate_summary(text)

            st.header("📝 Smart Summary")
            st.markdown(summary)

            st.divider()
            st.subheader("💬 Ask Your Document")

            for turn in st.session_state.chat_history:
                with st.chat_message(turn["role"]):
                    st.markdown(turn["content"])

            user_question = st.chat_input("What would you like to know?")
            if user_question:
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                with st.chat_message("user"):
                    st.markdown(user_question)

                with st.spinner("🔍 Analyzing..."):
                    try:
                        response = qa_engine.answer_question(text, user_question, st.session_state.chat_history)
                        st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
                        with st.chat_message("assistant"):
                            st.markdown(f"**Answer:** {response['answer']}")
                            st.markdown(f"📌 *Source:* {response['justification']}")
                    except Exception as e:
                        st.error(f"⚠️ Something went wrong: {e}")

        elif mode == "🧩 Challenge Me":
            st.header("🧩 Document Challenge")

            if st.button("🎯 Generate Questions"):
                with st.spinner("Generating questions..."):
                    st.session_state.challenge_questions = challenge_engine.generate_questions(text)

            if "challenge_questions" in st.session_state:
                for idx, q in enumerate(st.session_state.challenge_questions):
                    st.markdown(f"**Q{idx + 1}:** {q}")
                    user_ans = st.text_input(f"Your Answer:", key=f"user_answer_{idx}")

                    if user_ans:
                        with st.spinner("Evaluating..."):
                            feedback = challenge_engine.evaluate_answer(text, q, user_ans)
                            st.markdown("📣 **Feedback:**")
                            st.info(feedback)

else:
    st.markdown(
    "<div style='text-align: center; font-size: 18px;'>📝 <em>Upload a document to begin using your smart assistant.</em></div>",
    unsafe_allow_html=True
)

