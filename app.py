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

@app.route('/alerts-page')
def alerts_page():
    return render_template('alerts_page.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    url = 'https://nonprd-arlo.instana.io/api/application-monitoring/analyze/traces'
    payload = request.get_json()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'apitoken pncHtgATRjep2fo0poggJQ'
    }

    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

@app.route('/api/events', methods=['GET'])
def events():
    url = 'https://nonprd-arlo.instana.io/api/events'
    headers = {
        'Authorization': 'apitoken pncHtgATRjep2fo0poggJQ'
    }

    response = requests.get(url, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
