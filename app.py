from flask import Flask, jsonify, render_template_string, request, session, redirect, url_for, send_file

from pdf.pdf import PDF, TTS
from dotenv import load_dotenv
import os
from flask_cors import CORS


"""Load env environment variables as os environment variables"""
load_dotenv()

""""Set up flask application"""
app = Flask(__name__)

app.secret_key = 'SECRET_KEY'
app.config["UPLOAD_FOLDER"] = "./data/"
CORS(app)
cache = {}

import uuid

# Testing code above
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if not request.files:
            return "no file uploaded", 400
        file = request.files['pdf']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return "invalid filename", 400
        
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            pdf_obj = PDF(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), 0, os.getenv("GPT3_API_KEY"))
            key = uuid.uuid1()
            cache[key] = pdf_obj
            return jsonify(
                key=key,
                status="success"
            )

        return "Unable to perform operation"


@app.route("/generate-transcript", methods=["POST"])
def generate_transcript():
    if request.method == "POST":
        key = request.args.get("key")
        pdf = cache[key]
        simp_text = pdf.generateTranscript()

        return jsonify(
            simpText=simp_text
        )

@app.route("/speech", methods=['POST'])
def speech():
    speech_obj = TTS(request.form['transcript'])
    return send_file(speech_obj.textToSpeech())

