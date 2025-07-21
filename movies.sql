import streamlit as st

st.title("Movie Booking System")

menu = ["Home", "Register", "Login", "Book Ticket"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.header("Welcome to the Movie Booking App!")
    # Show movies, search, etc.

elif choice == "Register":
    st.header("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        # Save to database (use sqlite3)
        st.success("Registration successful! Please log in.")

elif choice == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Check credentials
        st.success("Login successful!")

elif choice == "Book Ticket":
    st.header("Book a Ticket")
    # Show booking form, etc. 