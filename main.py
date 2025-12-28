from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/base')
def base():
    return render_template("base.html")