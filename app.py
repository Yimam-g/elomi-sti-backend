from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/diagnose', methods=['POST'])
def diagnose():
    symptoms = request.json.get('symptoms', '')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert STI diagnosis assistant."},
                {"role": "user", "content": f"Based on these symptoms: {symptoms}, what is the most likely STI and urgency level (high, medium, low)?"}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify(diagnosis=reply.split('\n')[0], urgency=reply.split('\n')[1])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
