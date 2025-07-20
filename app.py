from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/diagnose', methods=['POST'])
def diagnose():
    symptoms = request.json.get('symptoms', '')
    print("Symptoms received:", symptoms)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert STI diagnosis assistant."},
                {"role": "user", "content": f"Patient symptoms: {symptoms}. What is the likely STI and urgency (high, medium, low)?"}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
        diagnosis_lines = reply.split('\n')
        return jsonify(
            diagnosis=diagnosis_lines[0] if len(diagnosis_lines) > 0 else "Unclear",
            urgency=diagnosis_lines[1] if len(diagnosis_lines) > 1 else "Unknown"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ This is what Render needs to keep the app running:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
