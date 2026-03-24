import streamlit as st

def display():
    with st.sidebar:
        st.image("https://picsum.photos/250/80", width=250)
        st.title("Project 01: Dự đoán giá nhà & phát hiện bất thường")
        st.page_link(label="Home", page="pages/home.py")
        st.page_link(label="Business Problem", page="pages/business_problem.py")
        st.page_link(label="Task Assignment", page="pages/task-assignment.py")