# Chat Bot Project

This project is a chatbot system that utilizes various files for its database, source code, test cases, and outputs.
It is built with Python and includes a virtual environment setup for easy installation of dependencies.

## Prerequisites

Before you start, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) (>= 3.6)
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)

## Setup and Installation

Follow the steps below to set up the project on your local machine:

### 1. Clone the Repository
First, clone the repository to your local machine using the following command:
```
git clone git@github.com:kailash2058/chat_bot.git
cd chat_bot
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate (for linux)
venv\Scripts\activate (for windows)
```
3.Install the required libraries:

```
pip install requirnments.txt 
```
4.  Set up environment variables: for storing thr gemini api key

Create a .env file in the project root with the details mentioned in `.env` file.

5. Browse to the source code directiory and run the application by:
   
```
cd src
streamlit streamlit_ui.py
```


##Project structure
.
├── appointment_model
│   ├── exact_date.py
│   ├── __pycache__
│   └── validation.py
├── main_bot.py
├── rag_model
│   ├── doc_rag.py
│   ├── input_handler.py
│   ├── main.py
│   ├── __pycache__
│   └── query.py
├── streamlit_ui.py
├── st_test.py
└── test_case.xlsx


# Features of the Chatbot

## 1. Document-Based Query Answering
- The chatbot is capable of answering user queries by retrieving information from any given document. It provides accurate and context-aware
  responses based on the content of the documents.

## 2. Conversational Form for User Information
- The chatbot includes an interactive conversational form to collect user information (Name, Phone Number, Email) when prompted by the user. For example, when the user requests the chatbot to "call me," the
  form ensures that all the necessary information is gathered in a conversational manner.

## 3. Appointment Booking Integration
- The chatbot integrates with a conversational form to allow users to book appointments. This feature enables users to specify their preferred date and time in natural language.
   The system then processes the input and converts it into a standardized date format (YYYY-MM-DD).

## 4. Date Extraction and Validation
- Using tool-agents, the chatbot extracts dates mentioned in user queries (e.g., "Next Monday", today, tomorrow,in X day) and converts them into the correct format (YYYY-MM-DD).
  Additionally, the system validates user input for other critical information, such as verifying email addresses and phone numbers, ensuring the information is accurate and in the correct format.

## 5. Error Handling and Validation
- The chatbot handles potential errors in user input and prompts users to correct invalid data. For example, it will ask users to re-enter their phone number or email if the input is not in a valid format.

## 6. Seamless Integration with LLMs
- The chatbot integrates Gemini (or we can use any other preferred LLMs) to perform robust document retrieval, natural language understanding, and conversational dialogue. This makes the chatbot capable
  of answering a wide range of questions and handling user interactions effectively.

## 7. Scalability and Adaptability
- The chatbot is designed to scale as new documents and tools are added. It can easily be adapted to handle different types of conversational forms and integrate additional functionalities in the future.

## 8. User-friendly Interface
- The chatbot provides a user-friendly interface that allows users to interact effortlessly, either to ask questions from documents or to fill out forms for scheduling appointments and providing contact details.




