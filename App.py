import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama

class OllamaEmbeddingWrapper:
    def embed_documents(self, texts):
        return [ollama.embeddings(model="nomic-embed-text", prompt=text)['embedding'] for text in texts]
    def __call__(self, text):
        return ollama.embeddings(model="nomic-embed-text", prompt=text)['embedding']

def get_vectorstore(url): 
    # scraping the url to text
    web_loader = WebBaseLoader(url)
    document = web_loader.load()

    #splitting the text 
    splitter = RecursiveCharacterTextSplitter()
    chunks = splitter.split_documents(document)

    return chunks 

def get_response(prompt):
    return "Yes I agree"

def main():
    st.set_page_config(page_icon=":genie:",page_title="WebGenie")
    st.title("WebGenie :genie:")

    if "chat_history" not in st.session_state: 
        st.session_state.chat_history = [
            HumanMessage("Hello what are you ?"),
            AIMessage("Hello Am the WebGenie how can I help you!!"),
        ]

    with st.sidebar: 
        st.subheader(":gear: Settings")
        url = st.text_input(":link: Enter URL :")

    if url == None or url == "": 
        st.info(":warning: Please provide a URL to Enable chatting.")
    else : 
        docs = get_vectorstore(url)
        prompt = st.chat_input("type your prompt here...")
        if prompt != None and prompt != "": 
            st.session_state.chat_history.append(HumanMessage(prompt))
            st.session_state.chat_history.append(AIMessage(get_response(prompt,url)))

        for message in st.session_state.chat_history: 
            if isinstance(message,AIMessage): 
                with st.chat_message("AI"): 
                    st.write(message.content)
            elif isinstance(message,HumanMessage): 
                with st.chat_message("Human"): 
                    st.write(message.content)

        with st.sidebar: 
            st.write(docs)

if __name__ == "__main__": 
    main()