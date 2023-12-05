import os

import cons


from flask import Flask, request, jsonify, render_template

from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

app = Flask(__name__)

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = cons.APIKEY

# Initialize your VectorstoreIndexCreator
loader = DirectoryLoader(".", glob="*.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

@app.route('/')
def home():
    # You can render your HTML template here
    return render_template('index.html')import cons

import os
import sqlite3
from flask import Flask, request, jsonify, render_template


from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = cons.APIKEY

# Initialize your VectorstoreIndexCreator
loader = DirectoryLoader(".", glob="*.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect('feedback.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the "feedback" table
def create_feedback_table():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                generated_response TEXT NOT NULL,
                feedback_score INTEGER NOT NULL
            )
        ''')
        print("Table 'feedback' created or already exists.")

# Function to log errors
def log_error(exception, message):
    # Log the error details, you can replace this with your preferred logging mechanism
    print(f"Error: {exception}, Message: {message}")

# Endpoint for the default root path
@app.route('/')
def home():
    # You can render your HTML template here
    return render_template('index.html')

# Endpoint for collecting feedback
@app.route('/collect_feedback', methods=['POST'])
def collect_feedback():
    try:
        data = request.get_json()

        # Validate input
        if 'input' not in data or 'response' not in data or 'score' not in data:
            return jsonify({'error': 'Invalid input. Required fields: input, response, score'}), 400

        input_text = data['input']
        generated_response = data['response']
        feedback_score = data['score']

        # Validate score
        if not isinstance(feedback_score, int) or feedback_score not in [-1, 0, 1]:
            return jsonify({'error': 'Invalid score. Score should be -1, 0, or 1'}), 400

        # Store feedback in the database
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO feedback (input_text, generated_response, feedback_score)
                VALUES (?, ?, ?)
            ''', (input_text, generated_response, feedback_score))

        return jsonify({'message': 'Feedback collected successfully'})

    except Exception as e:
        log_error(e, "Error collecting feedback")
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint for generating a response
@app.route('/generate_response', methods=['POST'])
def generate_response_endpoint():
    try:
        data = request.get_json()

        # Validate input
        if 'text' not in data:
            return jsonify({'error': 'Invalid input. Required field: text'}), 400

        input_text = data['text']

        # Get response from your model
        results = index.query(input_text)
        response = results

        # Add the user's input and model's response to the conversation
        conversation = [{"role": "user", "content": input_text}, {"role": "llm", "content": response}]

        return jsonify({'response': response, 'conversation': conversation})

    except Exception as e:
        log_error(e, "Error generating response")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    create_feedback_table()
    app.run(debug=True)

@app.route('/generate_response', methods=['POST'])
def generate_response():
    if request.method == 'POST':
        input_text = request.json.get('text')
        results = index.query(input_text, llm=ChatOpenAI())

        # You may want to do some post-processing on the results before returning the response

        response = results  # Replace with your response generation logic

        return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)


