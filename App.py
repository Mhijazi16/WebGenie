from pydantic.v1.schema import schema
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama 
from langchain.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings 
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

llm = Ollama(model="llama3")

def get_retriever(url): 
    # scraping the url to text
    web_loader = WebBaseLoader(url)
    document = web_loader.load()

    #splitting the text 
    splitter = RecursiveCharacterTextSplitter()
    chunks = splitter.split_documents(document)

    #creating vectorstore 
    store = FAISS.from_documents(chunks,
                             embedding=OllamaEmbeddings(model="nomic-embed-text"))
    # returning a retriever 
    return store.as_retriever() 

def get_response(prompt,retriever):

    with st.spinner("retriever in progress"):
        info = retriever.invoke(prompt)

    template = f"""
        You are the WebGenie an AI assistant that scrapes URL then answers 
        questions based on the context you have.
        You need to use Markdown and emoji's when you output results
        here is the Context : {info}
        here is the question : {prompt}
    """

    with st.spinner("genereating response"):
        return llm.stream(template)

def main():
    st.set_page_config(page_icon=":genie:",page_title="WebGenie")
    st.title("WebGenie :genie:")

    if "chat_history" not in st.session_state: 
        st.session_state.chat_history = [
            HumanMessage("Explain What you do ?"),
        ]

    with st.sidebar: 
        st.subheader(":gear: Settings")
        url = st.text_input(":link: Enter URL :")

    if url == None or url == "": 
        st.info(":warning: Please provide a URL to Enable chatting.")

    if "retriever" not in st.session_state: 
        st.session_state.retriever = None
    else : 
        if st.session_state.retriever == None :
            st.session_state.retriever = get_retriever(url) 

        prompt = st.chat_input("type your prompt here...")

        if prompt != None and prompt != "": 
            st.session_state.chat_history.append(HumanMessage(prompt))


        for message in st.session_state.chat_history: 
            if isinstance(message,AIMessage): 
                with st.chat_message("AI"): 
                    res = st.write(get_response(prompt,st.session_state.retriever))
            elif isinstance(message,HumanMessage): 
                with st.chat_message("Human"): 
                    st.write(message.content)


if __name__ == "__main__": 
    main()
