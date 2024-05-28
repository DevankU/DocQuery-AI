
# DocQuery AI
Overview
DocQuery AI is a  Gradio-based web application that allows users to input a URL or upload a PDF and ask questions related to the content. The application retrieves relevant information from the provided document and generates answers using advanced natural language processing techniques.

It is basically Chat With RTX but can run on vram of less than 8GB

Features
1. URL Input: Users can provide a URL to a webpage, and the application will extract and analyze the content to answer questions.
2. PDF Upload: Users can upload a PDF document, and the application will process the content to respond to queries.
Question Answering: The application leverages language models to generate accurate answers based on the content of the provided document.                    
3. Interactive Interface: A user-friendly interface powered by Gradio allows for easy interaction and question submission.

## How it Works

Loading Documents:

For URLs: The WebBaseLoader is used to fetch and parse the content from the provided URL.
For PDFs: The PyPDFLoader is used to load and extract text from the uploaded PDF file.
Text Splitting:

The content from the document is split into manageable chunks using the RecursiveCharacterTextSplitter. This ensures that the text is processed in sections that are optimal for embedding and retrieval.
Embedding:

The text chunks are converted into vector embeddings using the OllamaEmbeddings model ("mistral"). These embeddings represent the semantic meaning of the text in a high-dimensional space.
Vector Store:

The vector embeddings are stored in a Chroma vector store, which allows for efficient retrieval of relevant chunks based on the user's query.
Retrieval:

When a question is asked, the application retrieves the most relevant chunks of text from the vector store using the user's query as a reference.
Answer Generation:

The retrieved text chunks are formatted into a context for the language model. The ollama.chat function uses the "mistral" model to generate a response based on the context and the user's question.
User Interaction:

The Gradio interface collects user input (URL, PDF, and question) and displays the generated answers.
## Installation

1) clone this repo

2) create a virtual enviroment 
```bash
    python -m venv .env
```
3) install requirements
```bash
pip install -r requirements.txt
```
4) install ollama
5) run " ollama run mistral" (this will download the mistral locally into your pc.)
6) run 
```bash
python main.py
```
