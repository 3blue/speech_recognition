from datetime import datetime
from flask import Flask, render_template, request
from . import app

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return render_template("home.html") + foo()
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


def foo():
    return "I sat by the Ocean"