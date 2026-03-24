import streamlit as st
import components.sidebar as sidebar

def main():
    sidebar.display()
    st.write("This is the Home page")
    
main()