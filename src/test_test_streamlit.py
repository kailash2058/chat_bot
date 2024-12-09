import streamlit as st
import pandas as pd
import os

# Import the validation and extraction functions
from appointment.validation import validate_email, validate_phone
from appointment.exact_date import extract_date
from rag_model.query import query_doc

# Function to save the appointment details to CSV
def save_to_csv(name, phone, email, appointment_date):
    file_name = '../outputs/appointment.csv'

    # Check if the file exists
    if os.path.isfile(file_name):
        # If file exists, load it into a DataFrame
        df = pd.read_csv(file_name)
    else:
        # If file doesn't exist, create an empty DataFrame with headers
        df = pd.DataFrame(columns=['Name', 'Phone', 'Email', 'Appointment Date'])

    # Create a new DataFrame for the new row of data
    new_data = pd.DataFrame({'Name': [name], 'Phone': [phone], 'Email': [email], 'Appointment Date': [appointment_date]})

    # Concatenate the existing DataFrame with the new data
    df = pd.concat([df, new_data], ignore_index=True)

    # Save the updated DataFrame back to CSV
    df.to_csv(file_name, index=False)

# Function to handle chatbot responses
def chatbot_response(query):
    if not query.strip():  # If the query is empty or contains only spaces
        return "Please enter a valid query."

    if "call me" in query.lower():
        # Trigger conversational form for details
        return "Sure! May I know your Name, Phone Number, and Email to schedule a call?"
    else:
        # Process document-based queries
        query_doc(query)
        return "I'm processing your document-related query..."

# Streamlit UI layout
def main():
    st.title("Appointment Booking Chatbot")
    st.subheader("Ask me anything about documents or schedule a call!")

    # Initialize session state variables if not already set
    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.name = ""
        st.session_state.phone = ""
        st.session_state.email = ""
        st.session_state.appointment_date = ""

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("What can I do for you today?")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate bot response
        response = chatbot_response(user_input)

        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Handle booking flow
        if "May I know your name" in response or "call me" in user_input.lower():
            st.session_state.step = 1
            st.session_state.name = ""
            st.session_state.phone = ""
            st.session_state.email = ""
            st.session_state.appointment_date = ""

        # Step 1: Ask for Name
        if st.session_state.step == 1:
            st.write("Bot: May I know your name?")
            st.session_state.name = st.text_input("Your Name:")
            if st.session_state.name:
                st.session_state.step += 1

        # Step 2: Ask for Phone Number
        elif st.session_state.step == 2:
            st.write(f"Bot: Hello {st.session_state.name}, can you provide your phone number?")
            st.session_state.phone = st.text_input("Your Phone Number:")
            if st.session_state.phone:
                if validate_phone(st.session_state.phone):
                    st.session_state.step += 1
                else:
                    st.warning("Please provide a valid phone number (10-15 digits, optional '+').")

        # Step 3: Ask for Email
        elif st.session_state.step == 3:
            st.write("Bot: What is your email address?")
            st.session_state.email = st.text_input("Your Email:")
            if st.session_state.email:
                if validate_email(st.session_state.email):
                    st.session_state.step += 1
                else:
                    st.warning("Please provide a valid email (e.g., example@domain.com).")

        # Step 4: Ask for Appointment Date
        elif st.session_state.step == 4:
            st.write("Bot: When would you like to schedule the appointment?")
            date_query = st.text_input("Date for the appointment:")
            if date_query:
                st.session_state.appointment_date = extract_date(date_query) or date_query
                st.session_state.step += 1

        # Step 5: Confirm Appointment and Save
        elif st.session_state.step == 5:
            st.write(f"Bot: Confirming your appointment details:\n"
                     f"Name: {st.session_state.name}\n"
                     f"Phone: {st.session_state.phone}\n"
                     f"Email: {st.session_state.email}\n"
                     f"Appointment Date: {st.session_state.appointment_date}")
            if st.button("Confirm Appointment"):
                booking_response = f"Appointment booked for:\n" \
                                   f"Name: {st.session_state.name}\n" \
                                   f"Phone: {st.session_state.phone}\n" \
                                   f"Email: {st.session_state.email}\n" \
                                   f"Scheduled for: {st.session_state.appointment_date}"
                st.success(booking_response)
                save_to_csv(st.session_state.name, st.session_state.phone, st.session_state.email, st.session_state.appointment_date)
                st.session_state.step = 1  # Reset for a new booking

        # Step 6: Exit/Start Again
        elif st.session_state.step == 6:
            st.write("Bot: Thank you for using the appointment booking system!")
            if st.button("Start New Appointment"):
                st.session_state.step = 1  # Restart the process

# Run the app
if __name__ == "__main__":
    main()
