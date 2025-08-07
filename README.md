# 🧠 Memory-Enabled Agentic Chatbot with LangGraph

This is a **memory-enabled AI chatbot** built using [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://www.langchain.com/), OpenAI models, and Chroma vectorstore.

The chatbot can:
- 🧠 Store user-shared facts in memory (e.g., "I use Figma for design").
- 🔄 Update existing memories.
- 🔍 Retrieve top-5 relevant memories (with similarity threshold).
- 💬 Answer questions using retrieved memory + LLM.

## 🧩 Features
- **Agentic Workflow**: Built using LangGraph with distinct stateful nodes for storing, retrieving, and reasoning.
- **Vector Memory**: Embedding-based memory storage and retrieval via `Chroma`.
- **Intelligent Intent Detection**: Store, update, or query memory based on LLM-determined intent.
- **Front-end UI**: Clean ChatGPT-style chat UI with Streamlit.
- **API Interface**: Flask-powered REST API to connect with the front-end.

## 🛠️ Folder Structure
```
.
├── app.py               # Flask API that calls LangGraph workflow
├── main.py              # Core LangGraph graph definition
├── frontend_code.py      # Streamlit chat front-end (ChatGPT style)
├── requirements.txt     # All required Python dependencies
├── .env                 # Environment variables (add your OpenAI API key here)
└── README.md            # This file
```

## 🚀 Getting Started

### 1. Clone the repo
```
git clone https://github.com/your-username/agentic-memory-chatbot.git
cd agentic-memory-chatbot
```
### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Set your OpenAI key in .env
```
OPENAI_API_KEY=api_key_here
```

## 🧠 Run the System

### 1. Start the Flask API
```
python app.py
```
This will run at: `http://localhost:5000/chat`

### 2. Launch the Streamlit Front-End
```
streamlit run streamlit_ui.py
```
