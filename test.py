import streamlit as st
from questions import questions

st.title("Interview Preparation Application")

# Initialize session state variables
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = 0

# Function to start quiz


def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.question_index = 0
    st.session_state.correct_answers = 0
    st.session_state.incorrect_answers = 0
    st.rerun()


# Display topic and difficulty level selection if quiz has not started
if not st.session_state.quiz_started:
    st.session_state.topic = st.selectbox(
        "Select a topic to prepare for interview",
        options=['Deep Learning', 'Data Science',
                 'Machine Learning', 'Generative AI']
    )
    st.session_state.difficulty_level = st.selectbox(
        "Select your difficulty level",
        options=['Easy', 'Intermediate', 'Advanced']
    )

    # Display instructions
    st.header("Instructions")
    st.markdown(
        "Select an option to begin the quiz. After selecting an option, questions will be displayed one by one.")

    # Display start quiz button
    if st.button("Start Quiz"):
        start_quiz()

# Function to check the user's answer and update the state


def check_answer():
    selected_option = st.session_state.selected_option
    current_question = questions[st.session_state.question_index]
    for option in current_question['options']:
        if option['text'] == selected_option:
            if option['isCorrect']:
                st.session_state.correct_answers += 1
                st.success("Correct!")
            else:
                st.session_state.incorrect_answers += 1
                st.error("Incorrect!")
            break

    # Move to the next question
    st.session_state.question_index += 1
    # Rerun the app to display the next question
    st.rerun()

# Display the current question


def show_next_question():
    if st.session_state.question_index < len(questions):
        current_question = questions[st.session_state.question_index]
        st.write(current_question['question'])

        options = [option['text'] for option in current_question['options']]
        st.radio("Choose an option:", options, key='selected_option')

        if st.button("Submit"):
            check_answer()
    else:
        st.write("Quiz completed!")
        st.write(f"Correct answers: {st.session_state.correct_answers}")
        st.write(f"Incorrect answers: {st.session_state.incorrect_answers}")


# Display questions if quiz has started
if st.session_state.quiz_started:
    st.header("Multiple Choice Questions")
    show_next_question()
