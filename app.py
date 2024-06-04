from flask import Flask, jsonify, request, render_template
import requests
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data-page')
def data_page():
    return render_template('data_page.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # This endpoint will act as a proxy to the given API
    url = 'https://nonprd-arlo.instana.io/api/application-monitoring/analyze/traces'
    payload = request.get_json()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'apitoken pncHtgATRjep2fo0poggJQ'
    }

    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
