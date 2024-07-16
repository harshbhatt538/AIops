import os
import requests
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import timedelta
import logging

# Load environment variables from a .env file or set them in the environment
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
def home():
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
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)

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
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'username': user.username, 'email': user.email})
            response = jsonify(access_token=access_token)
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        logging.error('Error during login: %s', e)
        return jsonify({'error': 'An error occurred during login'}), 500



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


@app.route('/chart-page')
@jwt_required()
def chart_page():
    return render_template('chart_page.html')


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


if __name__ == '__main__':
    app.run(debug=True)
