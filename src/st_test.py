import streamlit as st
import pandas as pd
import os
from appointment.validation import validate_email, validate_phone
from appointment.exact_date import extract_date
from rag_model.query import query_doc
import random
import time

# Function to save appointment details to CSV
def save_to_csv(name, phone, email, appointment_date):
    file_name = 'appointment.csv'

    if os.path.isfile(file_name):
        df = pd.read_csv(file_name)
    else:
        df = pd.DataFrame(columns=['Name', 'Phone', 'Email', 'Appointment Date'])

    new_data = pd.DataFrame({'Name': [name], 'Phone': [phone], 'Email': [email], 'Appointment Date': [appointment_date]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_name, index=False)

# Function to handle chatbot responses (without unnecessary repetition)
def response_generator(query):
    response = ""
    if "call me" in query.lower():
        response = "Sure! Let's begin by asking for your Name, Phone Number, and Email to schedule a call."
    else:
        response = query_doc(query)  # Assuming query_doc processes the document query and returns relevant info
    
    return response



def book_appointment(name, phone, email, appointment_date):
    """
    Function to book an appointment by collecting user details and saving them to a CSV file.
    """
    save_to_csv(name, phone, email, appointment_date)
    booking_response = f"Appointment booked for:\nName: {name}\nPhone: {phone}\nEmail: {email}\nScheduled for: {appointment_date}"
    return booking_response

# Streamlit UI layout
def main():
    st.title("Appointment Booking Chatbot")
    st.subheader("Welcome! I can help you schedule appointments or answer document-related queries.")

    # Initialize session state variables if not already set
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "step" not in st.session_state:
        st.session_state.step = 1  # Start with the first question
        st.session_state.name = ""
        st.session_state.phone = ""
        st.session_state.email = ""
        st.session_state.appointment_date = ""

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input and trigger assistant responses
    prompt = st.chat_input("What can I do for you today?")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate assistant response based on user input
        response = response_generator(prompt)  # Assume you have a response generator

        # Display assistant response in chat
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Triggering Appointment Booking Flow
        if "May I know your name" in response or "call me" in prompt.lower():
            st.session_state.step = 1
            st.session_state.name = ""
            st.session_state.phone = ""
            st.session_state.email = ""
            st.session_state.appointment_date = ""

        # Step 1: Ask for Name
        if st.session_state.step == 1:
            st.write("Bot: May I know your name?")
            st.session_state.name = st.text_input("Your Name:", key="name_input")
            if st.session_state.name:
                st.session_state.step += 1  # Move to the next step

        # Step 2: Ask for Phone Number
        elif st.session_state.step == 2:
            st.write(f"Bot: Hello {st.session_state.name}, can you provide your phone number?")
            st.session_state.phone = st.text_input("Your Phone Number:", key="phone_input")
            if st.session_state.phone:
                if validate_phone(st.session_state.phone):
                    st.session_state.step += 1  # Move to the next step
                else:
                    st.warning("Please provide a valid phone number (10-15 digits, optional '+').")

        # Step 3: Ask for Email
        elif st.session_state.step == 3:
            st.write("Bot: What is your email address?")
            st.session_state.email = st.text_input("Your Email:", key="email_input")
            if st.session_state.email:
                if validate_email(st.session_state.email):
                    st.session_state.step += 1  # Move to the next step
                else:
                    st.warning("Please provide a valid email (e.g., example@domain.com).")

        # Step 4: Ask for Appointment Date
        elif st.session_state.step == 4:
            st.write("Bot: When would you like to schedule the appointment?")
            date_query = st.text_input("Date for the appointment:", key="date_input")
            if date_query:
                st.session_state.appointment_date = extract_date(date_query) or date_query
                st.session_state.step += 1  # Move to the next step

        # Step 5: Confirm Appointment and Save
        elif st.session_state.step == 5:
            st.write(f"Bot: Confirming your appointment details:\n"
                     f"Name: {st.session_state.name}\n"
                     f"Phone: {st.session_state.phone}\n"
                     f"Email: {st.session_state.email}\n"
                     f"Appointment Date: {st.session_state.appointment_date}")
            if st.button("Confirm Appointment"):
                booking_response = book_appointment(
                    st.session_state.name,
                    st.session_state.phone,
                    st.session_state.email,
                    st.session_state.appointment_date
                )
                st.success(booking_response)
                st.session_state.step = 1  # Reset for a new booking

        # Step 6: Exit/Start Again
        elif st.session_state.step == 6:
            st.write("Bot: Thank you for using the appointment booking system!")
            if st.button("Start New Appointment"):
                st.session_state.step = 1  # Restart the process

# Ensure the script is executed directly
if __name__ == "__main__":
    main()