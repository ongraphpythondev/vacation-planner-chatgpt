from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import streamlit as st
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from openai import AuthenticationError


template = """
I want you to act as a travel guide. I will tell you a location and duration of travel
and you would need to come up with an itinerary for that duration. I will be travelling
with {companion}. So you need to keep the choices of places accordingly. The trip needs
to be budget friendly as well as laidback. Also suggest me famous restaurants to try at those 
places. Finally, create the itinerary along with total cost per person. Let's do this for 
{location} for a duration of {days} days
"""
prompt = PromptTemplate(
    input_variables=["companion", "location", "days"],
    template=template,
)


def handleClick():
    system_prompt_message = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt_message])
    result = chat(chat_prompt.format_prompt(companion=companion,
                                            location=location, days=days).to_messages())



with st.container():
    st.header('Vacation Planner',divider=True)
    subheading = st.subheader("Enter you Open Api Keys in the sidebar")
    ''' The ultimate vacation planner will create a perfect itnerary for you. Just give the 
    name of country and duration. Oh! and do mention whom are you travelling with'''

with st.sidebar:
    OPENAI_API_KEY = st.text_input(
        '**Enter OpenAI API Key 🔑**' ,placeholder='Paste your key(🔑) here',type='password')
    if OPENAI_API_KEY:
        subheading.empty()
        companion = st.selectbox(
            "Travelling with", ("Noone", "Family", "Spouse", "Family with kids", "Friends"))
        location = st.text_input("Location")
        days = st.number_input("days", min_value=1, max_value=50)
        st.button('Submit', on_click=handleClick)

response = st.empty()
try:
    if OPENAI_API_KEY:
        chat = ChatOpenAI(streaming=True, callback_manager=CallbackManager(
            [StreamlitCallbackHandler(response)]), verbose=True, temperature=0,
            openai_api_key=OPENAI_API_KEY)
except AuthenticationError:
    st.error("Invalid OpenAI API Key")
