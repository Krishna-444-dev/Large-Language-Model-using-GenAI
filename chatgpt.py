'''import os
import sys

import cons

import chromadb

import streamlit as st

from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = cons.APIKEY

st.title('GPT Creator')
prompt = st.text_input('Enter your query here!')

if len(sys.argv) > 1:
    query = sys.argv[1]
    print(query)

    #loader = TextLoader("data.txt")
    loader = DirectoryLoader(".", glob = "*.txt")

    # index = VectorstoreIndexCreator().from_loaders([loader])

    print("Before creating the VectorstoreIndexCreator instance.")
    print("loader:", loader)

    index = VectorstoreIndexCreator().from_loaders([loader])

    print("After creating the VectorstoreIndexCreator instance.")

    results = index.query(query)
    print(results)  # Print the results of the query
else:
    print("Please provide a command-line argument.") '''






'''import os
import sys

import cons

import chromadb

import streamlit as st

from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = cons.APIKEY

st.title('GPT Creator')
prompt = st.text_input('Enter your query here!')

# Check if a prompt is provided
if prompt:
    # Define the directory where your text files are stored
    data_directory = "."

    # Create a VectorstoreLoader based on the data directory
    loader = DirectoryLoader(data_directory, glob="*.txt")

    # Create the VectorstoreIndex using the loader
    index = VectorstoreIndexCreator().from_loaders([loader])

    # Query the index with the user's prompt using ChatOpenAI
    results = index.query(prompt, llm=ChatOpenAI())

    # Display the results
    st.write("Results:")
    for result in results:
        st.write(result)
else:
    st.write("Please enter a query in the input box above.")'''





'''# Define 'ids' as an empty list
ids = []

# Add elements to 'ids' as needed
ids.append(1)
ids.append(2)
ids.append(3)

if len(ids) > 0:
    if isinstance(ids[0], (int, float)):
        import os
        import streamlit as st

        import cons

        from langchain.document_loaders import DirectoryLoader
        from langchain.indexes import VectorstoreIndexCreator

        # Set the OpenAI API key
        os.environ["OPENAI_API_KEY"] = cons.APIKEY

        st.title('GPT Creator')
        prompt = st.text_input('Enter your query here!')

        if prompt:
            # Use Streamlit to input queries

            # Use the DirectoryLoader to load text files in the current directory
            loader = DirectoryLoader(".", glob="*.txt")

            # Check if loader is not empty
            if loader:
                st.write("Indexing documents...")
                # Create a VectorstoreIndex from the loader
                index = VectorstoreIndexCreator().from_loaders([loader])
                st.write("Indexing complete.")

                # Query the index with the user's input
                results = index.query(prompt)

                if results:
                    # Display the results in a Streamlit table
                    st.write("Search results:")
                    st.table(results)

                else:
                    st.write("No results found for the query.")

            else:
                st.write("No documents found for indexing.")

        else:
            st.write("Please enter a query in the input box.")
    else:
        print("IDs are not of the expected type.")
else:
    print("No IDs found in the data.")'''



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
    return render_template('index.html')

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


