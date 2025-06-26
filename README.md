Your all-in-one GenAI-powered research companion that can:

Parse and summarize uploaded documents

Answer custom questions about them

Generate logic-based quiz questions

Evaluate your answers with feedback





**This is a strucutre for my code.**

 Layer -- 	                         Component --	                                       Purpose
 
📁 app.py --	                    Streamlit UI	  --	                               Main frontend, controls sidebar, user input, layout

📁 backend/parser.py --	        extract_text()   --	                             	Reads and extracts raw text from uploaded PDFs or .txt

📁 backend/summarizer.py --		    generate_summary()	 --	                            Sends raw doc to LLM to return TL;DR-style summary

📁 backend/qa_engine.py --		        answer_question()  --	                           	Handles Q&A from doc using FAISS + LLM prompt

📁 backend/challenge_engine.py	generate_questions() / evaluate_answer()	 --	   Quiz generator and feedback engine

📁 utils/retrieval.py --		        split_text(), build_faiss_index(), search_top_k()  --	   	Vector-based chunk search logic

📁 utils/validator.py --		        is_answer_plausible()	  --	                        Checks how grounded a response is in context (using difflib)

📦 Model API	 --	                Mistral-7B via OpenRouter	 --	                     Handles summarization, question answering, and evaluation





**concept of working of m model**

🔁 **Flow Example: "Summarize + Ask"**
User uploads a file → extract_text() reads it

Text gets summarized → generate_summary()

User asks a question → stored in st.session_state.chat_history

qa_engine.py:

Breaks document into chunks

Finds top similar chunks with FAISS

Builds LLM prompt with context + history

Sends prompt to Mistral

Returns answer + justification (top chunk)

Session state keeps the full back-and-forth chat memory





🧩 **Flow Example: "Challenge Me"**
App sends context (first 5 chunks) to LLM → generates MCQ-style questions

User answers → evaluation prompt is sent

LLM judges the answer and gives feedback

Validator soft-checks whether that feedback matches context



Setup Instructions

Create and activate a virtual environment

**(Python 3.11.9 recommended)**

python -m venv venv

source venv/bin/activate  # or venv\Scripts\activate on Windows





Install required dependencies
pip install -r requirements.txt


Run the app
streamlit run app.py





                      ┌────────────────────────────┐
                      │     📄 Uploaded Document    │
                      └────────────┬───────────────┘
                                   │
                        Text Extraction (parser.py)
                                   │
                        ┌──────────▼───────────┐
                        │ generate_summary()   │ ← Summarizer (summarizer.py)
                        └──────────────────────┘
                                   │
        ┌────────────────────────────────────────────────────┐
        │                                                    │
        ▼                                                    ▼
 Q&A Mode (qa_engine.py)                            Challenge Mode (challenge_engine.py)
        │                                                    │
  Split into chunks                                Extract 5 chunks
  Build prompt w/ chat history                     Prompt LLM for questions
  Retrieve top-k similar context                   Let user answer → Evaluate
  Send to Mistral (OpenRouter)                     Soft-check answer grounding
        │                                                    │
        ▼                                                    ▼
 Return answer + source                          Return feedback
        │
 Silent plausibility checker (validator.py)





in theo , explained above 

smart-research-assistant/
│
├── app.py                         # Main Streamlit UI logic
│
├── backend/
│   ├── parser.py                  # Extracts text from PDFs and text files
│   ├── summarizer.py              # Summarizes text using OpenRouter
│   ├── qa_engine.py               # Handles Q&A using document + chat history
│   └── challenge_engine.py        # Generates and evaluates logic questions
│
├── utils/
│   ├── retrieval.py               # Chunk splitter and context retriever
│   └── validator.py               # Checks LLM outputs for hallucination
│
├── .streamlit/
│   └── secrets.toml               # (optional) API key storage
│
└── requirements.txt               # Python dependencies


Built by Nilanchal Upadhyay




