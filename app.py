from mcq.mcq_generation import mcq_generation, generate
import streamlit as st
GROQ_API = st.secrets["GROQ_API"]
# API = st.secrets["GOOGLE_API"]

st.markdown(
    """
    <style>
    .question-text {
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #4C3BCF;
        border-radius: 5px;
    }
    .answer-text {
        font-size: 16px;
        padding: 8px;
        margin-bottom: 5px;
        border-radius: 5px;
    }
    .correct-answer {
        background-color: #d4edda;
        color: #155724;
    }
    .incorrect-answer {
        background-color: #f8d7da;
        color: #721c24;
    }
    .summary {
        border-top: 1px solid #e0e0e0;
        padding-top: 10px;
        margin-top: 20px;
    }
    .completion-message {
        font-size: 20px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 20px;
        text-align: center;
    }
    .stats {
        font-size: 18px;
        margin-bottom: 20px;
    }
    .summary-header {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    /* Custom CSS for radio buttons */
    .stRadio > div {
        padding: 10px;
        font-size: 18px;
    }
    .stRadio div[role='radiogroup'] {
        display: flex;
        flex-direction: column;
    }
    .stRadio label {
        background-color: #071952; /* Change this to your desired color */
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def initialize_state():
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'incorrect_answers' not in st.session_state:
        st.session_state.incorrect_answers = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []


initialize_state()


def state_variables():
    st.session_state.quiz_started = False
    st.session_state.question_index = 0
    st.session_state.correct_answers = 0
    st.session_state.incorrect_answers = 0
    st.session_state.user_answers = []


def reset_state():
    state_variables()
    st.session_state.questions = []
    st.rerun()


def retake():
    state_variables()
    st.session_state.quiz_started = True
    st.rerun()


def start_quiz():
    state_variables()
    st.session_state.quiz_started = True
    st.session_state.questions = generate(
        topic=st.session_state.topic,
        level=st.session_state.difficulty_level,
        number_of_questions=st.session_state.num_questions,
        API=GROQ_API
    )
    print(st.session_state.questions)
    st.rerun()


def check_answer():
    selected_option = st.session_state.selected_option
    current_question = st.session_state.questions[st.session_state.question_index]
    correct_option = next(
        option['text'] for option in current_question['options'] if option['isCorrect'])
    st.session_state.user_answers.append({
        'question': current_question['question'],
        'selected_option': selected_option,
        'correct_option': correct_option
    })
    if correct_option == selected_option:
        st.session_state.correct_answers += 1
    else:
        st.session_state.incorrect_answers += 1
    st.session_state.question_index += 1
    st.rerun()


def show_question():
    current_question = st.session_state.questions[st.session_state.question_index]
    st.markdown(
        f'<div class="question-text">{current_question["question"]}</div>', unsafe_allow_html=True)
    # Ensure all options have 'text' key
    options = [option['text']
               for option in current_question['options'] if 'text' in option]

    if not options:
        st.error("Invalid question format. No valid options available.")
        st.rerun()
        # return
    st.radio("Choose an option:", options,
             key='selected_option', label_visibility='hidden')
    if st.button("Submit"):
        check_answer()


def display_summary():
    st.markdown(
        '<div class="completion-message">Quiz completed!</div>', unsafe_allow_html=True)
    stats_col1, stats_col2 = st.columns(2)
    with stats_col1:
        st.markdown('<div class="stat-box"><div class="stat-header">Correct Answers</div><div class="stat-value">{}</div></div>'.format(
            st.session_state.correct_answers), unsafe_allow_html=True)
    with stats_col2:
        st.markdown('<div class="stat-box"><div class="stat-header">Incorrect Answers</div><div class="stat-value">{}</div></div>'.format(
            st.session_state.incorrect_answers), unsafe_allow_html=True)

    # Display the summary of all questions and answers
    st.markdown(
        '<div class="summary-header">Summary of your answers:</div>', unsafe_allow_html=True)
    for answer in st.session_state.user_answers:
        st.write(f"**Question:** {answer['question']}")
        if answer['selected_option'] == answer['correct_option']:
            st.success(f"**Your answer:** {answer['selected_option']}")
        else:
            st.success(f"**Correct answer:** {answer['correct_option']}")
            st.error(f"**Your answer:** {answer['selected_option']}")
        st.write("---")
    if st.button("Retake Quiz"):
        retake()
    if st.button("Go to Home Screen"):
        reset_state()


if not st.session_state.quiz_started:
    st.title("Interview Preparation Application")
    st.session_state.topic = st.selectbox("Select a topic", [
                                          'Deep Learning', 'Data Science', 'Machine Learning', 'Generative AI'])
    st.session_state.difficulty_level = st.selectbox(
        "Select difficulty level", ['Easy', 'Intermediate', 'Advanced'])
    st.session_state.num_questions = st.number_input(
        "Select number of questions", min_value=5, max_value=30, value=10, step=5)
    if st.button("Start Quiz"):
        start_quiz()
else:
    total_questions = len(st.session_state.questions)
    progress = st.session_state.question_index / total_questions
    st.progress(progress)
    st.write(
        f"Question {st.session_state.question_index} of {total_questions}")

    if st.session_state.question_index < total_questions:
        show_question()
    else:
        display_summary()
