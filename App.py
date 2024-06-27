import streamlit as st

def get_response(prompt):
    pass

def main():
    st.set_page_config(page_icon=":genie:",page_title="WebGenie")
    st.title("WebGenie :genie:")

    with st.sidebar: 
        st.subheader(":gear: Settings")
        url = st.text_input(":link: Enter URL :")

    prompt = st.chat_input("type your prompt here...")
    with st.chat_message("Human"): 
        st.write(prompt)
    with st.chat_message("AI"): 
        st.write(get_response(prompt))

if __name__ == "__main__": 
    main()