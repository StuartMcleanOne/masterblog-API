from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend endpoints (avoid CORS errors)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5002)
