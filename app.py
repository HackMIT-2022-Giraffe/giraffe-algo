from flask import Flask, render_template_string, request, session, redirect, url_for, send_file

from pdf.pdf import PDF, TTS
from dotenv import load_dotenv
import os

"""Load env environment variables as os environment variables"""
load_dotenv()

""""Set up flask application"""
app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# Testing code below



# Testing code above

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.form['uuid'] and request.form['pdf']:
        session['uuid'] = request.form['uuid']
        print("HI")
        
        pdf_obj = PDF(request.form['pdf'], 0, os.getenv('GPT3_API_KEY'))
        session['files'].append(pdf_obj)
        return "File successfully uploaded"
    else:
        return "Unable to perform operation, too few operands"

@app.route("/speech", methods=['POST'])
def transcript():
    speech_obj = TTS(request.form['transcript'])
    return send_file(speech_obj.textToSpeech())

@app.route("/", methods=['GET'])
def set_session():
    session['files'] = list()
    return "Session successfully set!"
