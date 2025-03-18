import streamlit as st
import time

from helpers.prepare_vector_db import create_vector_store_from_files
from helpers.conversation_chat import get_conversation_chain
from templates import css, bot_message_element, user_message_element


def render_messages(container):
    """Render chat messages in the chat container."""
    with container:
        chat_html = '<div id="chat-container" class="chat-container"">'
        for role, message in st.session_state.chat_history:
            template = user_message_element if role == "User" else bot_message_element
            chat_html += template.replace("{{MSG}}", message)
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)


def handle_user_input(user_input, chat_container):
    """Handle user input and generate chatbot responses."""
    if not st.session_state.conversation:
        return st.warning("Please upload and process your documents first.")

    st.session_state.chat_history.append(("User", user_input))

    render_messages(chat_container)

    response = st.session_state.conversation.invoke({"question": user_input})
    bot_reply = response["answer"]
    st.session_state.chat_history.append(("Bot", ""))

    full_response = ""
    for line in bot_reply.split("\n"):
        if line.strip() == "":
            full_response += "\n"
        else:
            for word in line.split():
                full_response += word + " "
                st.session_state.chat_history[-1] = ("Bot", full_response)
                render_messages(chat_container)
                time.sleep(0.04)
        full_response += "\n"

    st.session_state.chat_history[-1] = ("Bot", full_response)
    render_messages(chat_container)


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Chatbot Demo RAG", page_icon=":robot_face:", layout="wide"
    )
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.title("Chatbot Demo RAG")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.empty()

    def render_init_chat():
        if not st.session_state.chat_history or not st.session_state.conversation:
            chat_html = '<div class="chat-container">'
            chat_html += bot_message_element.replace(
                "{{MSG}}", "Welcome! Please upload your documents and ask a question."
            )
            chat_html += "</div>"
            chat_container.markdown(chat_html, unsafe_allow_html=True)
        else:
            render_messages(chat_container)

    render_init_chat()

    def handle_input():
        st.session_state.user_message_temp = st.session_state.user_message
        st.session_state.user_message = ""

    with st.container():
        _ = st.text_input(
            "Ask a question about your uploaded document:",
            placeholder="Type your question here",
            key="user_message",
            on_change=handle_input,
        )

    if "user_message_temp" in st.session_state and st.session_state.user_message_temp:
        handle_user_input(st.session_state.user_message_temp, chat_container)
        del st.session_state.user_message_temp

    with st.sidebar:
        st.subheader("Upload your documents")
        documents = st.file_uploader(
            "Upload PDFs here", accept_multiple_files=True, type="pdf"
        )
        if st.button("Process"):
            if documents:
                with st.spinner("Processing your documents..."):
                    vector_store = create_vector_store_from_files(documents)
                    st.session_state.conversation = get_conversation_chain(vector_store)
                    st.success("Documents processed successfully.")
            else:
                st.warning("Please upload your documents first.")


if __name__ == "__main__":
    main()
