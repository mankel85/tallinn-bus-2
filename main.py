from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Tere tulemast Tallinna liinide äppi!</h1>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)