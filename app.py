from flask import Flask, render_template, request
import openai
import speech_recognition as sr

app = Flask(__name__, template_folder="templates", static_folder="static")

# OpenAI API Key (Replace with your own)
openai.api_key = "sk-proj-XXXXX"

# Speech Recognition Function
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)  # Google Speech-to-Text API
        return text
    except sr.UnknownValueError:
        return "Speech not recognized. Please try again."
    except sr.RequestError:
        return "Speech Recognition API unavailable."

# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# Features Page
@app.route("/feature")
def feature():
    return render_template("feature.html")

# Technical Page
@app.route("/technical")
def technical():
    return render_template("technical.html")

# Dashboard Page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Login Page
@app.route("/login")
def login():
    return render_template("login.html")

# Signup Page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# Skill Evaluation
@app.route("/evaluate", methods=["POST"])
def evaluate():
    evaluation = None
    task_type = request.form.get("task_type")

    if task_type == "writing":
        essay = request.form.get("essay", "").strip()
        if not essay:
            evaluation = "⚠️ Please enter an essay for evaluation."
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Evaluate the essay based on grammar, coherence, vocabulary, and argument strength."},
                    {"role": "user", "content": f"Essay: {essay}"}
                ]
            )
            evaluation = response['choices'][0]['message']['content']

    elif task_type == "speaking":
        if "audio" not in request.files or request.files["audio"].filename == "":
            evaluation = "⚠️ No audio file uploaded. Please record and try again."
        else:
            audio_file = request.files["audio"]
            audio_text = speech_to_text(audio_file)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the spoken language based on fluency, pronunciation, grammar, and clarity."},
                    {"role": "user", "content": f"Transcribed Speech: {audio_text}"}
                ]
            )
            evaluation = response['choices'][0]['message']['content']

    return render_template("result.html", evaluation=evaluation)

if __name__ == "__main__":
    app.run(debug=True)
