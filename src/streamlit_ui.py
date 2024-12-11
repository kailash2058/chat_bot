import streamlit as st
import pandas as pd
import os
from appointment.validation import validate_email, validate_phone
from appointment.exact_date import extract_date 
from rag_model.query import query_doc
from rag_model import doc_rag

# Function to save appointment details to CSV
def save_to_csv(name, phone, email, appointment_date):
    file_name = '../outputs/appointment.csv'

    if os.path.isfile(file_name):
        df = pd.read_csv(file_name)
    else:
        df = pd.DataFrame(columns=['Name', 'Phone', 'Email', 'Appointment Date'])

    new_data = pd.DataFrame({'Name': [name], 'Phone': [phone], 'Email': [email], 'Appointment Date': [appointment_date]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_name, index=False)

# Function to handle chatbot responses
def chatbot_response(query):
    if not query.strip():
        return "Please enter a query."
    
    if "call me" in query.lower():
        return "Sure! Let's begin by asking for your Name, Phone Number, and Email to schedule a call."
    else:
        doc_info=query_doc(query)
        return doc_info

# Function to handle the appointment booking step by step
def book_appointment():
    if 'step' not in st.session_state:
        st.session_state.step = 0  # Start at step 0

    if st.session_state.step == 0:
        # Step 1: Ask for Name
        name = st.text_input("What's your name?")
        if name:
            st.session_state.name = name
            st.session_state.step = 1
            st.session_state.step_1_done = True  # Mark step 1 as done
            st.session_state.step_2_done = False  # Reset the next step flag
            st.session_state.step_3_done = False
            st.session_state.step_4_done = False

    elif st.session_state.step == 1:
        # Step 2: Ask for Phone Number
        phone = st.text_input("What's your phone number?")
        if phone and validate_phone(phone):
            st.session_state.phone = phone
            st.session_state.step = 2
            st.session_state.step_2_done = True
            st.session_state.step_3_done = False
            st.session_state.step_4_done = False
        elif phone:
            st.error("Please provide a valid phone number.")

    elif st.session_state.step == 2:
        # Step 3: Ask for Email
        email = st.text_input("What's your email?")
        if email and validate_email(email):
            st.session_state.email = email
            st.session_state.step = 3
            st.session_state.step_3_done = True
            st.session_state.step_4_done = False
        elif email:
            st.error("Please provide a valid email address.")

    elif st.session_state.step == 3:
        # Step 4: Ask for Appointment Date
        date_query = st.text_input("When would you like to schedule your appointment for ?(next<day> eg:next monday) OR (in X days) OR <YYYY-MM-DD> OR <today> OR <tomorrow>")
        appointment_date = extract_date(date_query) or date_query
       
        if appointment_date:
            st.session_state.appointment_date = appointment_date
            st.session_state.step = 4
            st.session_state.step_4_done = True
        elif date_query:
            st.error("Please provide a valid date.")

    elif st.session_state.step == 4:
        # Step 5: Confirm and Save Appointment
        if st.button("Confirm Appointment"):
            save_to_csv(st.session_state.name, st.session_state.phone, st.session_state.email, st.session_state.appointment_date)
            st.success(f"Appointment for {st.session_state.name} has been scheduled on {st.session_state.appointment_date}.")
            # Reset flow for new booking
            st.session_state.step = 0

# Streamlit UI layout
def main():
    st.title("Appointment Booking Chatbot")
    st.subheader("Welcome! I can help you schedule appointments or answer document-related queries.")
    
    # User input for chatbot interaction
    user_query = st.text_input("Ask me anything about the documents or schedule an appointment by typing : call me")

    if user_query:
        response = chatbot_response(user_query)
        st.write(f"Bot: {response}")

        if "May I know your" in response or "call me" in user_query.lower():
            book_appointment()
       


if __name__ == "__main__":
    main()
