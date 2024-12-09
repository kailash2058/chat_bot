
import sys
import os
import pandas as pd

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
 
from appointment.validation import validate_email, validate_phone
from appointment.exact_date import extract_date
from rag_model.query import query_doc
from rag_model import doc_rag
import os


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






# Function to reset the bot state
def reset_state():
    # You can reset internal variables or states here if necessary
        main(validate_email, validate_phone, extract_date)


def chatbot_response(query):
    if not query.strip():  # If the query is empty or contains only spaces
        print("Please enter a query.")
        return main(validate_email, validate_phone, extract_date)

    if "call me" in query.lower():
        # Trigger conversational form for details
        return "Sure! May I know your Name, Phone Number, and Email to schedule a call?"
    else:
        # Process document-based queries
        # query = input("Enter document related query: ")
        query_doc(query)

        return main(validate_email, validate_phone, extract_date)

def main(validate_email, validate_phone, extract_date):
    print("Welcome to the Chatbot! Ask me anything about the documents or schedule a call.")
    while True:
        user_query = input("You: ")
        
        if "exit" in user_query.lower():
            print("Goodbye!")
            break
        
        response = chatbot_response(user_query)
        print("Bot:", response)

        # If booking triggered
        if "May I know your" in response:
            name = input("Name: ")  # Collect name (no validation here as names can vary)

            # Validate phone number
            while True:
                phone = input("Phone: ")
                if validate_phone(phone):
                    break  # Exit the loop if the phone number is valid
                print("Bot: Please provide a valid phone number (10-15 digits, optional '+').")

            # Validate email address
            while True:
                email = input("Email: ")
                if validate_email(email):
                    break  # Exit the loop if the email address is valid
                print("Bot: Please provide a valid email (e.g., example@domain.com).")

            # print(extract_date("next monday"))  # Returns the date of the next Monday
            print("you can enter date in any format: tomorrow, today, in X days , YYYY-MM-DD , next <day>eg: next monday, Dec 25, 2024")  

            date_query = input("When should I schedule the call? ")
            appointment_date = extract_date(date_query) or date_query

            # booking_response = book_appointment(name, phone, email, appointment_date)
            # booking_response = print("Appointment of:" name, "\n","phone:" phone,"\n",  "email :"email, "\n", "is booked for the date:" appointment_date)
            booking_response = "Appointment of: " + name + "\n" + "Phone: " + phone + "\n" + "Email: " + email + "\n" + "is booked for the date: " + appointment_date
            print(booking_response)
            save_to_csv(name, phone, email, appointment_date)
            print("Bot:", booking_response)


if __name__ == "__main__":
    main(validate_email, validate_phone, extract_date)
