import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI

dotenv_path = 'env'
load_dotenv(dotenv_path)
GOOGLE_API = os.getenv('G_API')

llm = GoogleGenerativeAI(model="models/text-bison-001",
                         google_api_key=GOOGLE_API)

st.title("Interview Prepation Application")

topic = st.sidebar.selectbox("Select a topic to prepare for interview",
                             options=['Deep Learning', 'Data Science', 'Machine Learning', 'Generative AI'])

difficulty_level = st.sidebar.selectbox("Select your difficulty level",
                                        options=['Easy', 'Intermediate', 'Advanced'])


st.header("Multiple Choice Question")

mcq_statement = st.text_area(
    "What is the result of executing the following code?", height=100)
mcq_options = st.columns(2)
mcq_option1 = mcq_options[0].radio("Select an option", "Option A")
mcq_option2 = mcq_options[0].radio("Select an option", "Option B")
mcq_option3 = mcq_options[1].radio("Select an option", "Option C")
mcq_option4 = mcq_options[1].radio("Select an option", "Option D")


print('hello')
