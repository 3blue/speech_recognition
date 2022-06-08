import requests
import json
from datetime import datetime
from flask import Flask, render_template, request
from . import app
import azure.cognitiveservices.speech as speechsdk

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        response = query(request.form['question'], request.form['context'])
        response = ''.join( c for c in response if  c not in '[]",' )
        out = "THE MODEL SAYS: " + response
        return render_template("home.html") + out
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


def query(question, context):

    scoring_uri = 'http://a969e5da-ec26-4ceb-967c-4d8f2c25f65a.eastus.azurecontainer.io/score'
    key = 'MOdyhuXuBfxZFv04xWMyXB6ejMAcLKBv'

    # Set the appropriate headers
    headers = {"Content-Type": "application/json"}
    headers["Authorization"] = f"Bearer {key}"

    # Make the request and display the response and logs
    data = {
        "query": question,
        "context": context,
    }
    data = json.dumps(data)
    resp = requests.post(scoring_uri, data=data, headers=headers)
    return resp.text
    
def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription="6138afae6da245e19d77fd3beb8869aa", region="eastus")
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")