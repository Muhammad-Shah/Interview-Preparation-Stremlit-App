# import os
# from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pprint import pprint
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
import json
import random

# dotenv_path = 'env'
# load_dotenv(dotenv_path)
# GOOGLE_API = os.getenv('G_API')
# API = os.getenv('API')

# And a query intended to prompt a language model to populate the data structure.


class Option(BaseModel):
    text: str = Field(description="The text of the option")
    isCorrect: bool = Field(
        description="Indicator if the option is correct or not")

# Define your desired data structure for MCQs.


class MCQ(BaseModel):
    question: str = Field(description="The statement of the question")
    options: list[Option] = Field(
        description="List of answer options with correctness indicated")

# llm = GoogleGenerativeAI(model="models/text-bison-001",
#                          google_api_key=GOOGLE_API)


def chat_model(temperature, GROQ_API):
    return ChatGroq(temperature=temperature,
                    model_name="Llama3-70b-8192",
                    api_key=GROQ_API,
                    max_tokens=1000,
                    model_kwargs={
                        "top_p": 1,
                        "frequency_penalty": 0.5,
                        "presence_penalty": 0.5
                    }
                    )


def generate(level, topic, number_of_questions, API):
    generation_system_message_content = '''You are an expert in generating diverse and high-quality Multiple Choice Questions (MCQs) for interview preparation. 
    Your vast and comprehensive knowledge allows you to cover a wide range of topics without repetition. 
    You provide clear, concise, and relevant questions that are appropriately challenging based on the specified difficulty level. 
    Ensure that the questions are varied and never repeat the same question twice. Always return the response strictly in JSON format.\n\n'''

    human_message_content = '''
    **Generate Multiple Choice Questions (MCQs)**

    **Topic:** {topic}

    **Difficulty Level:** {level}

    **Number of questions:** {number_of_questions}

    **Instructions:** Generate {number_of_questions} multiple-choice questions (MCQ) on the topic of {topic} at the specified difficulty level. 
                    The questions should have four options, with one correct answer and three distractors. 
                    Ensure the questions are clear, concise, and relevant to the Topic. 
                    Return the MCQ in JSON format with the following structure:
                  
    ]

    {format_instructions}
    '''

    # Construct the prompt
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=generation_system_message_content),
        HumanMessagePromptTemplate.from_template(human_message_content)
    ])

    parser = JsonOutputParser(pydantic_object=MCQ)

    response = completion(prompt_template, level, topic,
                          number_of_questions, parser, API)
    return response


def completion(prompt, topic, defficulty_level, number_of_questions, parser, API):
    temp = random.uniform(0.1, 1)
    llm = chat_model(temp, API)
    llm_chain = prompt | llm | parser

    # Construct the parameters dictionary
    # parameters = {
    #     "query": prompt,
    #     # Add more parameters as needed
    # }

    parameters = {
        'level': defficulty_level,
        'topic': topic,
        'number_of_questions': number_of_questions,
        'format_instructions': parser.get_format_instructions()
    }

    # Remove None values from parameters
    response = llm_chain.invoke(parameters)
    return response


def mcq_generation(difficulty_level, topic, number_of_questions=10):
    return questions
