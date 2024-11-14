import streamlit as st
import requests
from fpdf import FPDF
import random

def save_to_pdf(questions, user_answers, correct_answers):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for i, (quest, user_ans, correct_ans) in enumerate(zip(questions, user_answers, correct_answers)):
            pdf.cell(200, 10, txt=f"Q{i + 1}: {quest['question']}", ln=True)
            pdf.cell(200, 10, txt=f"Your Answer: {user_ans}", ln=True)
            pdf.cell(200, 10, txt=f"Correct Answer: {correct_ans}", ln=True)
            pdf.cell(200, 10, txt=" ", ln=True)  # Add space between questions

        pdf.output("quiz_results.pdf")
        return "quiz_results.pdf"

st.set_page_config(page_title="Quiz Maker", layout="wide")

st.title("Quiz Maker")
st.divider()

num_of_questions = st.number_input("Number of Questions:", min_value=5, max_value=30)
category = st.selectbox("Select Category: ", ["General Knowledge", "Mythology", "Sports", "History", "Animals"])
difficulty_level = st.selectbox("Select Difficulty: ", ["Easy", "Medium", "Hard"])

load = st.button("Generate Quiz")
st.divider()

if load:
    st.header(f"Quiz on {category}")
    category_map = {
        "General Knowledge": 9,
        "Mythology": 20,
        "Sports": 21,
        "History": 23,
        "Animals": 27
    }
    category_id = category_map.get(category)

    api_url = f"https://opentdb.com/api.php?amount={num_of_questions}&category={category_id}&difficulty={difficulty_level.lower()}&type=multiple"
    response = requests.get(api_url, verify=False)
    questions = response.json().get("results", [])

    st.session_state.questions = questions
    st.session_state.user_answers = [None] * len(questions)
    
    correct_answers = [quest['correct_answer'] for quest in questions]
    st.session_state.correct_answers = correct_answers
    

if 'questions' in st.session_state:
    for i, quest in enumerate(st.session_state.questions):
        st.write(f"{i+1}. {quest['question']}")
        options = quest['incorrect_answers'] + [quest['correct_answer']]
        answer = st.radio("Select Answer: ", options=options, key=f"answer_{i}")
        
        st.session_state.user_answers[i] = answer
        

    submit = st.button("Submit Quiz")
    if submit:
        score = 0
        for i in range(len(st.session_state.user_answers)):
            if st.session_state.user_answers[i] == st.session_state.correct_answers[i]:
                score = score + 1
        
        total_questions = len(st.session_state.user_answers)
        st.markdown(f"### Your score is {score} out of {total_questions}")
        
    save = st.button("Save to PDF")
    
    if save:
        pdf_path = save_to_pdf(st.session_state.questions, st.session_state.user_answers, st.session_state.correct_answers)
        st.success("Quiz saved to PDF!")
        st.download_button(label="Download PDF", data=open(pdf_path, "rb"), file_name="quiz_results.pdf")
    
        
