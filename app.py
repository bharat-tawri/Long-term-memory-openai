# app.py
from flask import Flask, request, jsonify
from main import process_input
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'Message is required'}), 400

    try:
        response = process_input(user_input)
        return jsonify({'reply': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)