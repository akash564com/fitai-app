from flask import Flask, render_template, request, jsonify
import sqlite3
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
app.config['DATABASE'] = 'database.db'
app.config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

# Database initialization
def init_db():
    with app.app_context():
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        # Add other tables: meals, progress, etc.
        db.commit()

# OpenAI integration
def generate_workout_plan(goal, level, duration, equipment):
    prompt = f"Create a {duration}-minute {level} workout plan for {goal} using {equipment}. Include warmup and cooldown."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-workout', methods=['POST'])
def generate_workout():
    data = request.json
    plan = generate_workout_plan(
        data['goal'], 
        data['level'], 
        data['duration'], 
        data['equipment']
    )
    # Save to database
    return jsonify({'plan': plan})

# Add other routes: login, signup, save-progress, chatbot, etc.
from flask import Flask, render_template

app = Flask(__name__)

# User Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

# Admin Routes
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/lang/<language>')
def set_language(language):
    # Logic to set language preference
    return redirect(request.referrer or '/')
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
