# Richard Feynman Digital Twin

This project is an AI chatbot inspired by Richard Feynman's way of thinking and explaining things. The main idea was to create a chatbot that not only answers questions but also explains concepts in a simple and intuitive way, similar to how Feynman taught science.

## Features

* Richard Feynman inspired personality
* Custom knowledge base using RAG
* Different teaching styles
* Learning preference options
* Adjustable response length
* Conversation memory
* Feynman's Chalkboard mode
* Source citations
* Clear conversation option

## Technologies Used

* Python
* Streamlit
* Google Gemini API
* ChromaDB
* Sentence Transformers
* Retrieval-Augmented Generation (RAG)

## How It Works

1. The user asks a question.
2. The system searches a knowledge base made from Richard Feynman's writings.
3. Relevant information is retrieved from ChromaDB.
4. The retrieved context, user preferences, and Feynman persona are sent to Gemini.
5. Gemini generates a response based on that information.
6. The sources used are shown below the answer.

## What I Learned

This project helped me understand how AI applications work beyond just using an API. I learned how RAG systems retrieve information, how embeddings can be used to search a knowledge base, and how vector databases such as ChromaDB are used in real applications. I also got hands-on experience with prompt engineering, Streamlit, and putting different AI components together into one working project.

## Future Improvements

Some things I would like to add in the future:

* A more advanced chalkboard mode
* Better source display
* More personalisation options
* Further UI improvements
* Improved long-term memory

## Running the Project

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```
