#!/usr/bin/env python
# coding: utf-8

import openai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()


def controller(query_string):
    # Step 1 - Get your OpenAI API key
    openai.api_key = os.environ.get('OPENAI_KEY')
    file_name = "dmv_prompts.jsonl"
    # Step 2 - Upload training data
    upload_response = openai.File.create(
        file=open(file_name, "rb"),
        purpose='fine-tune'
    )
    file_id = upload_response.id
    # Fine-tune model
    fine_tune_response = openai.FineTune.create(
        training_file=file_id, model="davinci")
    fine_tuned_model = None
    if fine_tune_response.fine_tuned_model == None:
        fine_tuned_model = openai.FineTune.retrieve(
            id=fine_tune_response.id).fine_tuned_model

    # Get the response for the prompt received from the user
    new_prompt = query_string
    answer = openai.Completion.create(
        engine='davinci',
        model=fine_tuned_model,
        prompt=new_prompt,
        # Change the number depending on the required length of response.
        max_tokens=25,
        temperature=0
    )
    response = answer['choices'][0]['text']
    print("Response: ", answer)
    return response

# API routes


@app.route('/search', methods=['POST'])
def search():
    response = jsonify(controller(request.json['search_prompt']))
    response.headers.add('Access-Control-Allow-Origin',
                         'http://localhost:3000')
    return response


if __name__ == '__main__':
    app.run()
