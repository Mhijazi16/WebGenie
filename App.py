import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

def get_response(prompt):
    return "Yes I agree"

def main():
    st.set_page_config(page_icon=":genie:",page_title="WebGenie")
    st.title("WebGenie :genie:")

    if "chat_history" not in st.session_state: 
        st.session_state.chat_history = [
            AIMessage("Hello Am the WebGenie :genie: how can I help you !!")]

    with st.sidebar: 
        st.subheader(":gear: Settings")
        url = st.text_input(":link: Enter URL :")

    prompt = st.chat_input("type your prompt here...")
    if prompt is not None or prompt != "": 
        st.session_state.chat_history.append(HumanMessage(prompt))
        st.session_state.chat_history.append(AIMessage(get_response(prompt)))

    with st.chat_message("Human"): 
        st.write(prompt)
    with st.chat_message("AI"): 
        st.write(get_response(prompt))

    with st.sidebar: 
        st.write(st.session_state.chat_history)

if __name__ == "__main__": 
    main()