# Richard Feynman Digital Twin

A Digital Twin of Richard Feynman built using Gemini, ChromaDB, Streamlit, and Retrieval-Augmented Generation (RAG). The project aims to simulate Feynman's style of thinking and explaining concepts by combining a custom persona with information retrieved from a curated knowledge base of his interviews, quotes, and writings.

## Features

* Richard Feynman-inspired conversational persona
* Retrieval-Augmented Generation (RAG)
* Custom knowledge base built from interviews, quotes, and book excerpts
* Conversational memory during a session
* Streamlit-based chat interface
* Knowledge source display for transparency

## Tech Stack

* Python
* Google Gemini API
* Streamlit
* ChromaDB
* Sentence Transformers

## Project Structure

```text
app.py          # Main Streamlit application
ingest.py       # Processes and stores knowledge base documents
rag.py          # Retrieval logic
memory.py       # Memory utilities
persona.md      # Feynman persona definition
data/           # Interviews, quotes, and book excerpts
```

## Setup

1. Clone the repository

```bash
git clone <repository-url>
cd feynman-digital-twin
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

4. Build the knowledge base

```bash
python ingest.py
```

5. Run the application

```bash
python -m streamlit run app.py
```

## How It Works

When a user asks a question, the system first searches the knowledge base for relevant information. The retrieved content, conversation history, and Feynman persona are then provided to Gemini to generate a response. This helps produce answers that are both context-aware and aligned with Feynman's style.

## What I Learned

This project helped me understand how AI applications are built beyond just using an API. I learned how RAG works, how embeddings and ChromaDB help retrieve information from a knowledge base, and how conversational memory can improve interactions. I also got some practical experience with Streamlit and connecting different AI components into a single working system. Overall, it was a good hands-on learning experience and gave me a better understanding of how modern AI assistants work.
