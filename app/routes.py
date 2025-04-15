from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from app import db
from app.models import Admin, Event, Registration
import re
from functools import wraps

# Create blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__, url_prefix='/auth')
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Validation patterns
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_PATTERN = re.compile(r'^09\d{9}$')  # 11 digits starting with 09

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- Main Routes ----------
@main.route('/')
def index():
    # Get upcoming events, sorted by date
    upcoming_events = Event.query.filter(Event.event_date > datetime.utcnow()).order_by(Event.event_date).all()
    return render_template('index.html', events=upcoming_events)

@main.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if event has already started
    if event.has_started:
        flash('Registration for this event has closed', 'danger')
        return redirect(url_for('main.index'))
    
    # Check if event is full
    if event.is_full:
        flash('This event has reached its capacity', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Get form data
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename', '')
        school_name = request.form.get('school_name', '')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Validate required fields
        if not all([lastname, firstname, email, phone]):
            flash('Please fill all required fields', 'danger')
            return render_template('register.html', event=event)
        
        # Validate email format
        if not EMAIL_PATTERN.match(email):
            flash('Please enter a valid email address', 'danger')
            return render_template('register.html', event=event)
        
        # Validate phone format (09xxxxxxxxx)
        if not PHONE_PATTERN.match(phone):
            flash('Phone number must be 11 digits starting with 09', 'danger')
            return render_template('register.html', event=event)
        
        # Check if email already registered for this event
        existing_registration = Registration.query.filter_by(event_id=event_id, email=email).first()
        if existing_registration:
            flash('You have already registered for this event', 'danger')
            return render_template('register.html', event=event)
        
        # Create new registration
        registration = Registration(
            event_id=event_id,
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
            school_name=school_name,
            email=email,
            phone=phone
        )
        
        db.session.add(registration)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('register.html', event=event)

@main.route('/dbtest')
def dbtest():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({'status': 'success', 'message': 'Database connection successful'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'})

# ---------- Auth Routes ----------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            # Log failed login attempt
            flash('Invalid username or password', 'danger')
            
    return render_template('admin/login.html')

@auth.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))

# ---------- Admin Routes ----------
@admin.route('/dashboard')
@login_required
def dashboard():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('admin/dashboard.html', events=events)

@admin.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description', '')
        date_str = request.form.get('event_date')
        time_str = request.form.get('event_time')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        
        # Validate required fields
        if not all([title, date_str, time_str, location, capacity]):
            flash('Please fill all required fields', 'danger')
            return render_template('admin/add_event.html')
        
        try:
            # Parse date and time
            event_date = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
            
            # Check if date is in the future
            if event_date <= datetime.utcnow():
                flash('Event date must be in the future', 'danger')
                return render_template('admin/add_event.html')
            
            # Validate capacity is positive
            capacity = int(capacity)
            if capacity <= 0:
                flash('Capacity must be a positive number', 'danger')
                return render_template('admin/add_event.html')
                
            # Create new event
            event = Event(
                admin_id=session['admin_id'],
                title=title,
                description=description,
                event_date=event_date,
                location=location,
                capacity=capacity
            )
            
            db.session.add(event)
            db.session.commit()
            
            flash('Event created successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except ValueError:
            flash('Invalid date, time, or capacity', 'danger')
            return render_template('admin/add_event.html')
    
    return render_template('admin/add_event.html')

@admin.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description', '')
        date_str = request.form.get('event_date')
        time_str = request.form.get('event_time')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        
        # Validate required fields
        if not all([title, date_str, time_str, location, capacity]):
            flash('Please fill all required fields', 'danger')
            return render_template('admin/edit_event.html', event=event)
        
        try:
            # Parse date and time
            event_date = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
            
            # Validate capacity is positive
            capacity = int(capacity)
            if capacity <= 0:
                flash('Capacity must be a positive number', 'danger')
                return render_template('admin/edit_event.html', event=event)
            
            # If reducing capacity, make sure it's not less than current registrations
            if capacity < event.registration_count:
                flash(f'Capacity cannot be less than current registrations ({event.registration_count})', 'danger')
                return render_template('admin/edit_event.html', event=event)
                
            # Update event
            event.title = title
            event.description = description
            event.event_date = event_date
            event.location = location
            event.capacity = capacity
            
            db.session.commit()
            
            flash('Event updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except ValueError:
            flash('Invalid date, time, or capacity', 'danger')
            return render_template('admin/edit_event.html', event=event)
    
    return render_template('admin/edit_event.html', event=event)

@admin.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if event has already started
    if event.has_started:
        flash('Cannot delete an event that has already started', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Event deleted successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/events/<int:event_id>/registrations')
@login_required
def view_registrations(event_id):
    event = Event.query.get_or_404(event_id)
    registrations = Registration.query.filter_by(event_id=event_id).all()
    
    return render_template('admin/registrations.html', event=event, registrations=registrations) 