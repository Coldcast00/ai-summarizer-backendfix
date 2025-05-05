from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.json
    prompt = data.get("prompt", "")
    print("🟡 Received prompt:", prompt)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        result = response["choices"][0]["message"]["content"]
        print("🟢 Generated summary:", result)
        return jsonify({"summary": result})
    except Exception as e:
        print("🔴 OpenAI error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
