from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
import qrcode
import io
import base64
import json
import os
from functools import wraps

app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
if config_name == 'production':
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    if not app.config['SECRET_KEY']:
        raise ValueError("SECRET_KEY environment variable must be set in production")
else:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///edu_ride.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'driver'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Driver specific fields
    license_number = db.Column(db.String(50), nullable=True)
    vehicle_number = db.Column(db.String(20), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Student specific fields
    university = db.Column(db.String(100), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    pickup_location = db.Column(db.String(200), nullable=False)
    dropoff_location = db.Column(db.String(200), nullable=False)
    pickup_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, booked, in_progress, completed, cancelled
    fare = db.Column(db.Float, nullable=False)
    is_group_ride = db.Column(db.Boolean, default=False)
    max_passengers = db.Column(db.Integer, default=1)
    current_passengers = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    driver = db.relationship('User', foreign_keys=[driver_id], backref='driver_rides')
    student = db.relationship('User', foreign_keys=[student_id], backref='student_rides')

class GroupRide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ride = db.relationship('Ride', backref='group_members')
    student = db.relationship('User', backref='group_rides')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # 'upi', 'cash'
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    qr_code = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ride = db.relationship('Ride', backref='payments')
    student = db.relationship('User', backref='payments')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Debug: Print what we're looking for
        print(f"[DEBUG] Looking for user: {username}")
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"[SUCCESS] User found: {user.username}, Type: {user.user_type}")
            print(f"[DEBUG] Checking password...")
            
            if user.check_password(password):
                print(f"[SUCCESS] Password correct! Logging in...")
                login_user(user)
                flash(f'Welcome back, {user.username}!')
                
                if user.user_type == 'driver':
                    return redirect(url_for('driver_dashboard'))
                else:
                    return redirect(url_for('student_dashboard'))
            else:
                print(f"[ERROR] Password incorrect")
                flash('Invalid password')
        else:
            print(f"[ERROR] User not found: {username}")
            flash('User not found')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        user_type = request.form['user_type']
        
        print(f"[DEBUG] Registration attempt for: {username} ({user_type})")
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"[ERROR] Username already exists: {username}")
            flash('Username already exists')
            return render_template('register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print(f"[ERROR] Email already exists: {email}")
            flash('Email already exists')
            return render_template('register.html')
        
        try:
            user = User(
                username=username,
                email=email,
                phone=phone,
                user_type=user_type
            )
            user.set_password(password)
            
            # Add driver-specific fields
            if user_type == 'driver':
                user.license_number = request.form.get('license_number')
                user.vehicle_number = request.form.get('vehicle_number')
                print(f"[SUCCESS] Driver registered: {username}")
            else:
                user.university = request.form.get('university')
                print(f"[SUCCESS] Student registered: {username}")
            
            db.session.add(user)
            db.session.commit()
            
            print(f"[SUCCESS] User {username} registered successfully!")
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"[ERROR] Registration error: {e}")
            db.session.rollback()
            flash('Registration failed. Please try again.')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/debug/users')
def debug_users():
    """Debug route to see all users in database"""
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
            'created_at': user.created_at.isoformat() if user.created_at else None
        })
    return jsonify({'users': result, 'count': len(result)})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.user_type != 'student':
        return redirect(url_for('index'))
    
    available_rides = Ride.query.filter_by(status='available').all()
    return render_template('student_dashboard.html', rides=available_rides)

@app.route('/driver/dashboard')
@login_required
def driver_dashboard():
    if current_user.user_type != 'driver':
        return redirect(url_for('index'))
    
    my_rides = Ride.query.filter_by(driver_id=current_user.id).all()
    return render_template('driver_dashboard.html', rides=my_rides)

@app.route('/book_ride/<int:ride_id>')
@login_required
def book_ride(ride_id):
    if current_user.user_type != 'student':
        return redirect(url_for('index'))
    
    ride = Ride.query.get_or_404(ride_id)
    if ride.status != 'available':
        flash('This ride is no longer available')
        return redirect(url_for('student_dashboard'))
    
    ride.student_id = current_user.id
    ride.status = 'booked'
    db.session.commit()
    
    flash('Ride booked successfully!')
    return redirect(url_for('student_dashboard'))

@app.route('/create_ride', methods=['GET', 'POST'])
@login_required
def create_ride():
    if current_user.user_type != 'driver':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        pickup_location = request.form['pickup_location']
        dropoff_location = request.form['dropoff_location']
        pickup_time = datetime.strptime(request.form['pickup_time'], '%Y-%m-%dT%H:%M')
        fare = float(request.form['fare'])
        is_group_ride = 'is_group_ride' in request.form
        max_passengers = int(request.form.get('max_passengers', 1))
        
        ride = Ride(
            driver_id=current_user.id,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            pickup_time=pickup_time,
            fare=fare,
            is_group_ride=is_group_ride,
            max_passengers=max_passengers
        )
        
        db.session.add(ride)
        db.session.commit()
        
        flash('Ride created successfully!')
        return redirect(url_for('driver_dashboard'))
    
    return render_template('create_ride.html')

@app.route('/api/rides')
def api_rides():
    rides = Ride.query.filter_by(status='available').all()
    return jsonify([{
        'id': ride.id,
        'pickup_location': ride.pickup_location,
        'dropoff_location': ride.dropoff_location,
        'pickup_time': ride.pickup_time.isoformat(),
        'fare': ride.fare,
        'is_group_ride': ride.is_group_ride,
        'max_passengers': ride.max_passengers,
        'current_passengers': ride.current_passengers,
        'driver_name': ride.driver.username
    } for ride in rides])

@app.route('/api/book_ride', methods=['POST'])
@login_required
def api_book_ride():
    if current_user.user_type != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    ride_id = data.get('ride_id')
    ride = Ride.query.get_or_404(ride_id)
    
    if ride.status != 'available':
        return jsonify({'error': 'Ride not available'}), 400
    
    if ride.is_group_ride and ride.current_passengers >= ride.max_passengers:
        return jsonify({'error': 'Group ride is full'}), 400
    
    ride.student_id = current_user.id
    ride.status = 'booked'
    ride.current_passengers += 1
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Ride booked successfully'})

@app.route('/api/start_ride', methods=['POST'])
@login_required
def api_start_ride():
    if current_user.user_type != 'driver':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    ride_id = data.get('ride_id')
    ride = Ride.query.get_or_404(ride_id)
    
    if ride.driver_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if ride.status != 'booked':
        return jsonify({'error': 'Ride is not booked'}), 400
    
    ride.status = 'in_progress'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Ride started successfully'})

@app.route('/api/complete_ride', methods=['POST'])
@login_required
def api_complete_ride():
    if current_user.user_type != 'driver':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    ride_id = data.get('ride_id')
    ride = Ride.query.get_or_404(ride_id)
    
    if ride.driver_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if ride.status != 'in_progress':
        return jsonify({'error': 'Ride is not in progress'}), 400
    
    ride.status = 'completed'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Ride completed successfully'})

@app.route('/track_ride/<int:ride_id>')
@login_required
def track_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    return render_template('map_tracking.html', ride=ride)

@app.route('/api/notifications')
@login_required
def api_notifications():
    # Simple notification system - in production, use WebSockets or Server-Sent Events
    notifications = []
    
    if current_user.user_type == 'student':
        # Get notifications for students
        recent_rides = Ride.query.filter_by(student_id=current_user.id).order_by(Ride.created_at.desc()).limit(5).all()
        for ride in recent_rides:
            if ride.status == 'booked':
                notifications.append({
                    'type': 'info',
                    'message': f'Your ride from {ride.pickup_location} to {ride.dropoff_location} is confirmed!',
                    'timestamp': ride.created_at.isoformat()
                })
            elif ride.status == 'in_progress':
                notifications.append({
                    'type': 'success',
                    'message': f'Your ride is on the way! Driver: {ride.driver.username}',
                    'timestamp': ride.created_at.isoformat()
                })
    
    elif current_user.user_type == 'driver':
        # Get notifications for drivers
        recent_rides = Ride.query.filter_by(driver_id=current_user.id).order_by(Ride.created_at.desc()).limit(5).all()
        for ride in recent_rides:
            if ride.status == 'booked':
                notifications.append({
                    'type': 'info',
                    'message': f'New booking: {ride.pickup_location} to {ride.dropoff_location}',
                    'timestamp': ride.created_at.isoformat()
                })
    
    return jsonify(notifications)

@app.route('/generate_qr/<int:ride_id>')
@login_required
def generate_qr(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    
    # Create QR code data
    qr_data = {
        'ride_id': ride.id,
        'driver_id': ride.driver_id,
        'amount': ride.fare,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return render_template('qr_payment.html', qr_code=img_str, ride=ride)

if __name__ == '__main__':
    with app.app_context():
        try:
            # Drop all tables first to avoid conflicts
            db.drop_all()
            # Create all tables
            db.create_all()
            print("[SUCCESS] Database initialized successfully!")
        except Exception as e:
            print(f"[ERROR] Database initialization error: {e}")
            # Try to create tables anyway
            try:
                db.create_all()
                print("[SUCCESS] Database tables created!")
            except Exception as e2:
                print(f"[ERROR] Failed to create tables: {e2}")
    
    print("[INFO] Starting Edu-Ride application...")
    print("[INFO] Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
