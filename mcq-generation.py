import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI

dotenv_path = 'env'
load_dotenv(dotenv_path)
GOOGLE_API = os.getenv('G_API')
GOOGLE_API = st.secrets["G_API"]

llm = GoogleGenerativeAI(model="models/text-bison-001",
                         google_api_key=GOOGLE_API)


