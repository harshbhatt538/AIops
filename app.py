import os
import requests
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import timedelta
import logging
from collections import defaultdict
import time

logging.basicConfig(level=logging.INFO)

global_service_name = None

# Load environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'SUPER-SECRET-KEY')
DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://newuser:Hyb215215@localhost:3306/usresdb')
JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'SUPER-SECRET-KEY')

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Use cookies for storing JWT
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # Path for the access cookie
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF protection for simplicity (not recommended for production)

wsOneday = 86400000


class EpochTimeManager:
    def __init__(self):
        self.epoch_time_ms = None

    def update_time(self):
        self.epoch_time_ms = int(time.time() * 1000)

    def get_time(self):
        if self.epoch_time_ms is None:
            raise ValueError("Epoch time has not been set")
        return self.epoch_time_ms


time_manager = EpochTimeManager()
time_manager.update_time()  # Update the epoch time initially

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    services = db.Column(db.String(150), nullable=False, unique=True)


with app.app_context():
    db.create_all()


@app.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
        if existing_user:
            flash('Username or email already exists.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], email=data['email'], password=hashed_password),

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error('Error adding user: %s', e)
            return 'There was an issue adding the user', 500
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        response = jsonify(access_token=access_token)
        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
        return response
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/add_service', methods=['POST'])
@jwt_required()
def add_service():
    data = request.get_json()
    if not data or 'service_name' not in data:
        return jsonify({'message': 'Service name is required'}), 400

    service_name = data['service_name']
    new_service = Service(services=service_name)

    try:
        db.session.add(new_service)
        db.session.commit()
        return jsonify({"message": "Service added successfully",
                        "service": {"id": new_service.id, "services": new_service.services}}), 201
    except Exception as e:
        db.session.rollback()
        logging.error('Error adding service: %s', e)
        return jsonify({"message": "There was an issue adding the service", "error": str(e)}), 400


@app.route('/services', methods=['GET'])
@jwt_required()
def get_services():
    services = Service.query.all()
    service_data = [{'id': service.id, 'services': service.services} for service in services]
    return jsonify(services=service_data)


@app.route('/delete_service/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    service = Service.query.get_or_404(id)
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error('Error deleting service: %s', e)
        return jsonify({"message": "There was an issue deleting the service", "error": str(e)}), 400


@app.route('/data-page')
@jwt_required()
def data_page():
    return render_template('data_page.html')


@app.route('/alerts-page')
@jwt_required()
def alerts_page():
    return render_template('alerts_page.html')


@app.route('/chart-page', methods=['POST'])
@jwt_required()
def chart_page():
    data = request.get_json()
    service_name = data.get('service_name')

    if not service_name:
        return jsonify({'message': 'Service name is required'}), 400

    # Logic for handling the service name and generating the chart can go here

    global global_service_name
    global_service_name = service_name

    app.logger.info(f"Service Name: {global_service_name}")

    return render_template('chart_page.html', service_name=service_name)


@app.route('/modify-service')
@jwt_required()
def modify_service():
    return render_template('modify-services')


@app.route('/api/events', methods=['GET'])
@jwt_required()
def events():
    url = 'https://nonprd-arlo.instana.io/api/events'
    headers = {
        'Authorization': 'apitoken pncHtgATRjep2fo0poggJQ'
    }

    response = requests.get(url, headers=headers)
    return jsonify(response.json())


@app.route('/api/proxy', methods=['POST'])
@jwt_required()
def proxy():
    url = 'https://nonprd-arlo.instana.io/api/application-monitoring/analyze/traces'
    headers = {
        'Authorization': 'apitoken pncHtgATRjep2fo0poggJQ',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=request.json)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

    return jsonify(response.json())


@app.route('/api/5xx_errors', methods=['GET'])
def get_5xx_errors():
    logging.info("5xx errors endpoint hit")

    # Get the current epoch time
    current_epoch_time = time_manager.get_time()
    logging.info(f'Current epoch time: {current_epoch_time}')

    # Replace with your actual API request
    api_url = "https://nonprd-arlo.instana.io/api/application-monitoring/analyze/traces"
    headers = {
        "Authorization": "apitoken pncHtgATRjep2fo0poggJQ"
    }
    body = {
        "timeFrame": {
            "to": current_epoch_time,
            "focusedMoment": current_epoch_time,
            "autoRefresh": False,
            "windowSize": wsOneday
        },
        "tagFilterExpression": {
            "type": "EXPRESSION",
            "logicalOperator": "AND",
            "elements": [
                {
                    "type": "TAG_FILTER",
                    "name": "call.http.statusClass",
                    "operator": "EQUALS",
                    "entity": "NOT_APPLICABLE",
                    "value": "5xx"
                },
                {
                    "type": "TAG_FILTER",
                    "name": "application.name",
                    "operator": "EQUALS",
                    "entity": "DESTINATION",
                    "value": "GoldenDev Hmsdeviceevents"
                }
            ]
        },
        "metrics": [
            {
                "metric": "calls",
                "aggregation": "SUM"
            },
            {
                "metric": "errors",
                "aggregation": "MEAN"
            },
            {
                "metric": "latency",
                "aggregation": "MEAN"
            }
        ],
        "order": {
            "by": "timestamp",
            "direction": "ASC"
        },
        "group": {
            "groupbyTag": "endpoint.name",
            "groupbyTagEntity": "DESTINATION"
        },
        "includeInternal": False,
        "includeSynthetic": False
    }

    logging.info(f'Sending request to API: {api_url} with body: {body}')
    response = requests.post(api_url, headers=headers, json=body)
    data = response.json()

    logging.info(f'Raw API Data: {data}')

    # Initialize a dictionary to store hourly data counts
    hourly_data = defaultdict(int)

    # Time frame start (24 hours ago)
    time_frame_start = current_epoch_time - wsOneday

    logging.info(f'Time frame start: {time_frame_start}')

    # Iterate through the items and group them by hour within the last 24 hours
    for item in data.get("items", []):
        timestamp = item["trace"]["startTime"]

        # Check if the trace is within the last 24 hours
        if time_frame_start <= timestamp <= current_epoch_time:
            # Convert the timestamp to hour (considering IST timezone offset +05:30)
            hour = time.strftime('%H', time.gmtime((timestamp + 19800000) / 1000))
            hourly_data[hour] += 1  # Increment count for that hour

    # Generate a complete list of hours from the start to current time
    time_labels = []
    for i in range(24):
        label_hour = (time_frame_start + (i * 3600000)) // 1000
        time_labels.append(time.strftime('%H:00', time.gmtime((label_hour + 19800000))))

    # Convert to a list of dictionaries
    items = [{"hour": hour, "count": hourly_data.get(hour.split(':')[0], 0)} for hour in time_labels]

    logging.info(f'Processed Hourly Data: {items}')

    return jsonify(items)


if __name__ == '__main__':
    app.run(debug=True)
