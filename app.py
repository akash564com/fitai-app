from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
import sqlite3
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
app.config['DATABASE'] = 'database.db'
app.config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
# app.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
db = SQLAlchemy(app)




# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class ProgressLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    weight = db.Column(db.Float)
    calories_burned = db.Column(db.Float)
    workout_type = db.Column(db.String(50))
    workout_duration = db.Column(db.Integer)  # in minutes

class NutritionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    calories_consumed = db.Column(db.Float)

class AIUsageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    action_type = db.Column(db.String(20), nullable=False)  # 'chat', 'workout_gen', 'meal_plan'
    count = db.Column(db.Integer, default=1)

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
        CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE progress_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    weight REAL,
    calories_burned REAL,
    workout_type TEXT,
    workout_duration INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE nutrition_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    protein REAL,
    carbs REAL,
    fat REAL,
    calories_consumed REAL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE ai_usage_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    action_type TEXT NOT NULL,
    count INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
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
    return render_template('dashboard.html')

# API Endpoint for Dashboard Data
@app.route('/api/dashboard-data')
def dashboard_data():
    # In a real app, we'd get the current user from the session
    user_id = 1  # Example user
    
    # Calculate date ranges
    end_date = datetime.utcnow().date()
    start_date_week = end_date - timedelta(days=7)
    start_date_month = end_date - timedelta(days=30)
    
    # Weight data
    weight_logs = ProgressLog.query.filter(
        ProgressLog.user_id == user_id,
        ProgressLog.date >= start_date_month,
        ProgressLog.weight.isnot(None)
    ).order_by(ProgressLog.date).all()
    
    weight_data = [{
        'date': log.date.strftime('%Y-%m-%d'),
        'weight': log.weight
    } for log in weight_logs]
    
    # Workout frequency
    workout_logs = ProgressLog.query.filter(
        ProgressLog.user_id == user_id,
        ProgressLog.date >= start_date_week,
        ProgressLog.workout_type.isnot(None)
    ).all()
    
    # Calories burned
    calories_data = [{
        'date': log.date.strftime('%Y-%m-%d'),
        'calories': log.calories_burned
    } for log in workout_logs]
    
    # Macronutrients (average for the week)
    nutrition_logs = NutritionLog.query.filter(
        NutritionLog.user_id == user_id,
        NutritionLog.date >= start_date_week
    ).all()
    
    if nutrition_logs:
        avg_protein = sum(log.protein for log in nutrition_logs) / len(nutrition_logs)
        avg_carbs = sum(log.carbs for log in nutrition_logs) / len(nutrition_logs)
        avg_fat = sum(log.fat for log in nutrition_logs) / len(nutrition_logs)
    else:
        avg_protein = avg_carbs = avg_fat = 0
    
    # AI usage
    ai_usage = AIUsageLog.query.filter(
        AIUsageLog.user_id == user_id,
        AIUsageLog.date >= start_date_week
    ).all()
    
    # Return all data as JSON
    return jsonify({
        'weight_data': weight_data,
        'workout_frequency': len(workout_logs),
        'calories_data': calories_data,
        'macronutrients': {
            'protein': avg_protein,
            'carbs': avg_carbs,
            'fat': avg_fat
        },
        'ai_usage': {
            'chat': sum(log.count for log in ai_usage if log.action_type == 'chat'),
            'workout_gen': sum(log.count for log in ai_usage if log.action_type == 'workout_gen'),
            'meal_plan': sum(log.count for log in ai_usage if log.action_type == 'meal_plan')
        }
    })


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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
