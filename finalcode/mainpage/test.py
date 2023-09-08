# app.py (Flask app)
from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def execute_python_script():
    # Execute your Python script and capture the output
    script_output = subprocess.run(['python', 'spacetimecuberoutes/amsterdamnonpeakhour.py'], capture_output=True, text=True)
    result = script_output.stdout  # Assuming the result is text-based

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
