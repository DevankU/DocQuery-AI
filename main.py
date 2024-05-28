import gradio as gr
import bs4

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import ollama

from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader


def url_1(url):
    loader =WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict()
    )
    docs  = loader.load()

    text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits= text_splitter.split_documents(docs)

    embeddings= OllamaEmbeddings(model="mistral")

    vectorstore= Chroma.from_documents(documents=splits, embedding=embeddings)

    return vectorstore.as_retriever()


def pdf_1(pdf_path):
    loader =PyPDFLoader(pdf_path)

    docs = loader.load()
    text_splitter =RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    embeddings= OllamaEmbeddings(model="mistral")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    return vectorstore.as_retriever()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def  urlPaste(url, question):
    retriever = url_1(url)
    retrieved_docs = retriever.invoke(question)
    formatted_context = format_docs(retrieved_docs)

    formatted_prompt = f"Question: {question}\n\nContext: {formatted_context}"

    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']


def pdf_upload(pdf_file, question):
    retriever = pdf_1(pdf_file.name)
    retrieved_docs = retriever.invoke(question)

    formatted_context = format_docs(retrieved_docs)
    formatted_prompt = f"Question: {question}\n\nContext: {formatted_context}"
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])

    return response['message']['content']


iface=gr.Interface(
    fn=lambda url, pdf_file, question: pdf_upload(pdf_file, question) if pdf_file else urlPaste(url, question),
    inputs=[gr.Textbox(label="URL"), gr.File(label="Upload PDF"), gr.Textbox(label="Question")],
    
    outputs= gr.Textbox(),
    title = "RAG",

    description="Enter a URL or upload a PDF and ask your questions related to it."
)


iface.launch()