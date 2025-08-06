from flask import Flask, request, render_template, jsonify
import requests
import json

app = Flask(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = "AIzaSyD3NCLMy1tPVMcAY3t0NKyPZgH9GqbAtVg"

def generate_kql_from_prompt(natural_language):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
You are an expert in Microsoft Sentinel and Azure Log Analytics.
Convert the following natural language into an advanced KQL (Kusto Query Language) query with optimized filtering, aggregation, and joins if needed.
Respond with only the KQL query.

Natural Language:
{natural_language}
"""
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        try:
            result = response.json()
            kql = result['candidates'][0]['content']['parts'][0]['text']
            return kql.strip()
        except Exception as e:
            return "⚠️ Error parsing Gemini response"
    else:
        return f"⚠️ Gemini API error: {response.status_code}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_kql", methods=["POST"])
def generate_kql():
    data = request.get_json()
    natural_text = data.get("prompt", "")
    kql_result = generate_kql_from_prompt(natural_text)
    return jsonify({"kql": kql_result})

if __name__ == "__main__":
    app.run(debug=True)
