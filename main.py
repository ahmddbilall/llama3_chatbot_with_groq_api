import streamlit as st
from groq import Groq
from api import API_KEY


client = Groq(api_key=API_KEY)

def format_history(history):
    messages = []
    for message in history:
        role = message.get("role", "user")  # Default to 'user' if role is missing
        content = message.get("content", "")
        messages.append({"role": role, "content": content})
    return messages



def response(history):
    formatted_history = format_history(history)
    chat_completion = client.chat.completions.create(
            messages=formatted_history,
            model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content




st.set_page_config(page_title="Chat with llama3!",page_icon=":brain:",  layout="centered", )
st.title("🤖 Welcome Back Bilal!")
    

    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def translateRole(role):
    if role == 'human':
        return 'user'
    else:
        return 'assistant'


for message in st.session_state.chat_history:
    with st.chat_message(translateRole(list(message.keys())[0])):
        st.markdown(list(message.values())[0])



user_question = st.chat_input("Ask a question:")


if user_question:

    st.chat_message('user').markdown(user_question)

    st.session_state.chat_history.append({"role": "user", "content": user_question})
    
    response_text = response(st.session_state.chat_history)
    
    st.session_state.chat_history.append({"role":"assistant","content": response_text})
    
    st.chat_message('assistant').markdown(response_text)

