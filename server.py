# server.py
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Set up database connection and create table
def init_db():
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses (
                    role TEXT, importance TEXT, measures TEXT, ai_usage TEXT, 
                    ai_openness TEXT, challenges TEXT, vr_value TEXT, comments TEXT)''')
    conn.commit()
    conn.close()

# Route for the survey form
@app.route('/')
def survey():
    return render_template('survey.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    role = request.form.get('role')
    importance = request.form.get('importance')
    measures = ', '.join(request.form.getlist('measures'))
    ai_usage = request.form.get('ai_usage')
    ai_openness = request.form.get('ai_openness')
    challenges = ', '.join(request.form.getlist('challenges'))
    vr_value = request.form.get('vr_value')
    comments = request.form.get('comments')

    # Store response in database
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute("INSERT INTO responses (role, importance, measures, ai_usage, ai_openness, challenges, vr_value, comments) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (role, importance, measures, ai_usage, ai_openness, challenges, vr_value, comments))
    conn.commit()
    conn.close()

    return "Thank you for your response!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
