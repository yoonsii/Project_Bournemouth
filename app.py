from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import random

app = Flask(__name__)
CORS(app)

# Simulated exercises (in a real implementation, this would be more extensive and possibly stored in a database)
exercises = [
    {
        "prompt": "List all files in the current directory, including hidden files.",
        "solution": "ls -la",
        "verification": lambda output: "-rw-r--r--" in output and ".." in output
    },
    {
        "prompt": "Find all .txt files in the current directory and its subdirectories.",
        "solution": "find . -name '*.txt'",
        "verification": lambda output: ".txt" in output
    },
    # Add more exercises here
]

@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.json['command']
    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return jsonify({'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.output})

@app.route('/get_exercise', methods=['GET'])
def get_exercise():
    exercise = random.choice(exercises)
    return jsonify({'prompt': exercise['prompt']})

@app.route('/check_solution', methods=['POST'])
def check_solution():
    command = request.json['command']
    output = request.json['output']
    
    for exercise in exercises:
        if exercise['solution'] == command:
            if exercise['verification'](output):
                return jsonify({'correct': True, 'feedback': "Great job! That's the correct command and it produced the expected output."})
            else:
                return jsonify({'correct': False, 'feedback': "That's the right command, but the output doesn't look quite right. Make sure you're in the correct directory and try again."})
    
    return jsonify({'correct': False, 'feedback': "That doesn't seem to be the command we're looking for. Try again!"})

if __name__ == '__main__':
    app.run(debug=True)
