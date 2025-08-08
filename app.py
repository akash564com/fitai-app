from flask import Flask, render_template, request, jsonify
import sqlite3
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
app.config['DATABASE'] = 'database.db'
app.config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
# app.py
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    subscription_end = db.Column(db.DateTime)
    daily_chat_credits = db.Column(db.Integer, default=3)
    daily_workout_credits = db.Column(db.Integer, default=2)
    total_credits = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)

# Reset daily credits (cron job)
def reset_daily_credits():
    with app.app_context():
        users = User.query.filter_by(is_premium=False).all()
        for user in users:
            if user.last_reset.date() < datetime.utcnow().date():
                user.daily_chat_credits = 3
                user.daily_workout_credits = 2
                user.last_reset = datetime.utcnow()
        db.session.commit()


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

from flask import Flask, render_template, request, jsonify
import openai
import sqlite3
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# AI Chatbot Route
@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    user_input = request.json['message']
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a professional fitness coach"},
            {"role": "user", "content": user_input}
        ]
    )
    
    return jsonify({
        "text": response.choices[0].message['content'],
        "audio": text_to_speech(response.choices[0].message['content'])
    })

# Video Form Analysis (Mock)
@app.route('/video-form-check', methods=['POST'])
def form_check():
    # In production: Use OpenCV/Mediapipe for actual analysis
    # Mock response for demo
    feedback = [
        "Keep your back straight during squats",
        "Lower your hips parallel to the floor",
        "Widen your stance by 2 inches"
    ]
    return jsonify({"feedback": feedback})

# Habit Tracker
@app.route('/habit-tracker', methods=['GET'])
def habit_tracker():
    user_id = request.args.get('user_id')
    habits = get_user_habits(user_id)  # Fetch from SQLite
    
    analysis = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Analyze these fitness habits: {habits}. Give improvement suggestions."
    )
    
    return jsonify(analysis.choices[0].text)

# Calendar Generator
@app.route('/generate-calendar', methods=['POST'])
def generate_calendar():
    goal = request.json['goal']
    schedule = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Create weekly fitness schedule"},
            {"role": "user", "content": f"Goal: {goal}. Include workouts and meals"}
        ]
    )
    return jsonify(create_ics(schedule.choices[0].message['content']))

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    
    user = User.query.get(user_id)
    return render_template('dashboard.html', user=user)

# AI Feature Usage
@app.route('/use-ai-feature', methods=['POST'])
def use_ai_feature():
    data = request.json
    user_id = session.get('user_id')
    feature = data.get('feature')  # 'chat', 'workout', etc.
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(user_id)
    
    # Reset credits if needed
    if user.last_reset.date() < datetime.utcnow().date():
        reset_daily_credits()
    
    # Check credits
    if feature == 'chat':
        if user.is_premium or user.daily_chat_credits > 0:
            if not user.is_premium:
                user.daily_chat_credits -= 1
            # Process AI request here
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Daily limit reached', 'upgrade': True}), 402
    
    # Similar logic for other features...

# Subscription Route
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    user_id = session.get('user_id')
    plan = data.get('plan')  # 'monthly' or 'annual'
    
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(user_id)
    
    # In production: Verify payment with Stripe
    user.is_premium = True
    if plan == 'monthly':
        user.subscription_end = datetime.utcnow() + timedelta(days=30)
    else:  # annual
        user.subscription_end = datetime.utcnow() + timedelta(days=365)
    
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
