from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/base')
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)