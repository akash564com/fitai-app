from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import sqlite3
import openai
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_page(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/generate", methods=["POST"])
def generate_plan():
    data = request.json
    goal = data.get("goal")
    level = data.get("level")
    type = data.get("type")

    if not goal or not level or not type:
        return jsonify({"error": "Missing parameters"}), 400

    prompt = f"Create a personalized {type} plan for someone whose goal is '{goal}' and fitness level is '{level}'"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"result": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/progress", methods=["POST"])
def save_progress():
    data = request.json
    user = data.get("user")
    progress = data.get("progress")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO progress (user, data) VALUES (?, ?)", (user, progress))
    conn.commit()
    return jsonify({"status": "ok"})

@app.route("/api/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": msg}]
    )
    return jsonify({"reply": response.choices[0].message["content"]})

if __name__ == "__main__":
    app.run(debug=True, port=10000)
