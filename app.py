from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    target_value = db.Column(db.String(100), nullable=False)
    current_value = db.Column(db.String(100), default="0")
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Integer, default=0)

class ProgressLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)

class Streak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Mock user data (for demo)
current_user = {
    "id": 1,
    "username": "akash",
    "goals": [
        {
            "id": 1,
            "type": "Weight Loss",
            "target": "Lose 5kg",
            "deadline": "2023-07-01",
            "created_at": "2023-05-01",
            "progress": 65
        }
    ],
    "progress_logs": [
        {"date": "2023-05-01", "weight": 75.8, "bmi": 24.8},
        {"date": "2023-05-05", "weight": 75.2, "bmi": 24.6},
        {"date": "2023-05-10", "weight": 74.9, "bmi": 24.5},
        {"date": "2023-05-15", "weight": 74.5, "bmi": 24.4},
        {"date": "2023-05-20", "weight": 74.1, "bmi": 24.3},
        {"date": "2023-05-25", "weight": 73.8, "bmi": 24.2},
        {"date": "2023-05-30", "weight": 73.4, "bmi": 24.1},
        {"date": "2023-06-05", "weight": 73.0, "bmi": 24.0},
        {"date": "2023-06-10", "weight": 72.7, "bmi": 23.9},
        {"date": "2023-06-15", "weight": 72.5, "bmi": 24.1}
    ],
    "workout_logs": [
        {"date": "2023-06-10", "type": "Cardio", "duration": 45, "notes": "Morning run"},
        {"date": "2023-06-12", "type": "Strength", "duration": 60, "notes": "Upper body"},
        {"date": "2023-06-14", "type": "HIIT", "duration": 30, "notes": "Intense session"},
        {"date": "2023-06-15", "type": "Yoga", "duration": 40, "notes": "Evening stretch"}
    ],
    "streak": 7
}

@app.route('/')
def dashboard():
    return render_template('index.html', user_data=current_user)

@app.route('/update_metrics', methods=['POST'])
def update_metrics():
    weight = float(request.form['weight'])
    bmi = float(request.form['bmi'])
    
    # Add to progress logs
    today = datetime.now().strftime("%Y-%m-%d")
    current_user['progress_logs'].append({
        "date": today,
        "weight": weight,
        "bmi": bmi
    })
    
    return jsonify({"status": "success", "message": "Metrics updated!"})

@app.route('/log_workout', methods=['POST'])
def log_workout():
    workout_type = request.form['type']
    duration = int(request.form['duration'])
    notes = request.form['notes']
    
    # Add to workout logs
    today = datetime.now().strftime("%Y-%m-%d")
    current_user['workout_logs'].append({
        "date": today,
        "type": workout_type,
        "duration": duration,
        "notes": notes
    })
    
    # Update streak
    current_user['streak'] += 1
    
    return jsonify({"status": "success", "message": "Workout logged!"})

@app.route('/set_goal', methods=['POST'])
def set_goal():
    goal_type = request.form['type']
    target = request.form['target']
    deadline = request.form['deadline']
    
    # Create new goal
    new_goal = {
        "id": len(current_user['goals']) + 1,
        "type": goal_type,
        "target": target,
        "deadline": deadline,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "progress": 0
    }
    
    current_user['goals'].append(new_goal)
    
    return jsonify({"status": "success", "message": "New goal set!"})

@app.route('/get_progress_data')
def get_progress_data():
    # Prepare weight data for chart
    weight_data = [log['weight'] for log in current_user['progress_logs']]
    dates = [log['date'] for log in current_user['progress_logs']]
    
    return jsonify({
        "weights": weight_data,
        "dates": dates,
        "goal_progress": current_user['goals'][0]['progress'] if current_user['goals'] else 0
    })

@app.route('/get_ai_feedback')
def get_ai_feedback():
    # Simple AI logic to provide feedback
    weights = [log['weight'] for log in current_user['progress_logs']]
    last_weights = weights[-3:] if len(weights) >= 3 else weights
    
    feedback = ""
    suggestions = []
    
    if len(last_weights) >= 3:
        # Check for plateau
        if max(last_weights) - min(last_weights) < 0.5:
            feedback = "Hey Akash, I noticed your weight has remained steady for the past few days. Would you like to revise your workout plan to break through this plateau?"
            suggestions = [
                "Increase cardio by 20%",
                "Try intermittent fasting",
                "Adjust macro ratios"
            ]
        # Check for significant progress
        elif last_weights[-1] < last_weights[0] - 1.0:
            feedback = "Great progress Akash! You've lost significant weight recently. Keep up the good work!"
            suggestions = [
                "Maintain your current routine",
                "Add strength training to build muscle",
                "Reward yourself with a healthy treat"
            ]
        else:
            feedback = "You're making steady progress Akash. Consistency is key to reaching your goals!"
            suggestions = [
                "Track your calories more precisely",
                "Increase daily step count",
                "Try a new workout class for variety"
            ]
    else:
        feedback = "Welcome to FitTrack! Start logging your workouts and metrics to receive personalized feedback."
        suggestions = [
            "Set your first fitness goal",
            "Log your first workout",
            "Track your weight daily"
        ]
    
    return jsonify({
        "feedback": feedback,
        "suggestions": suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
