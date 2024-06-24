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


# Instructions:
# write code for 
