from flask import Flask, jsonify
import os

app = Flask(__name__)

# Placeholder data based on the Tkinter application structure
MOCK_WORKOUTS = {
    "Warm-up": [{"exercise": "Stretching", "duration": 10, "calories": 30}],
    "Workout": [{"exercise": "Running", "duration": 30, "calories": 300}],
    "Cool-down": [{"exercise": "Walking", "duration": 5, "calories": 15}]
}

# The version is dynamically set by the Jenkins pipeline
APP_VERSION = os.environ.get('APP_VERSION', 'V1.3.0-dev')

@app.route('/')
def hello_world():
    return f'<h1>ACEest Fitness & Gym Service - Version {APP_VERSION}</h1><p>Access /api/workouts to see mock data.</p>'

@app.route('/api/workouts')
def get_workouts():
    return jsonify(MOCK_WORKOUTS)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "OK", "version": APP_VERSION})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)