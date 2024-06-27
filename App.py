import streamlit as st

def main():
    st.set_page_config(page_icon=":genie:",page_title="WebGenie")
    st.title("WebGenie :genie:")

    with st.sidebar: 
        st.subheader(":gear: Settings")
        url = st.text_input(":link: Enter URL :")

if __name__ == "__main__": 
    main()