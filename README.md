# Event Registration System

A Flask-based web application for managing event registrations with an admin dashboard. This system allows organizations to publish events, collect registrations, and manage attendees through a simple and intuitive interface.

## Repository Details

**Purpose**: Simplify the event management process for organizations by providing a centralized platform for event registration.

**Key Features**:
- **Public event listings** - Display upcoming events with capacity tracking
- **Registration management** - Collect and store participant information
- **Admin dashboard** - Manage events and view registrations
- **User validation** - Email and phone validation with format enforcement
- **Data security** - Environment-based configuration for sensitive information
- **Audit trails** - Track which administrator created each event

**Technology Stack**:
- **Backend**: Flask, SQLAlchemy
- **Database**: MySQL/MariaDB via XAMPP
- **Frontend**: Bootstrap 5, HTML/CSS, JavaScript
- **Authentication**: Session-based admin login
- **Validation**: Client-side and server-side validation

**Target Users**: Schools, organizations, and clubs that need a simple system to manage event registrations without complex integrations.

## Features

- Public event listing and registration
- Admin panel for event management
- Event CRUD operations
- Registration management
- Responsive design

## Prerequisites

- Python 3.6 or higher
- XAMPP with MySQL/MariaDB
- pip (Python package manager)

## Setup

1. **Clone or download this repository**

2. **Install the required Python packages**

```bash
pip install flask flask-sqlalchemy mysql-connector-python python-dotenv
```

3. **Create the database**

- Start XAMPP and ensure MySQL service is running
- Open phpMyAdmin (http://localhost/phpmyadmin)
- Create a new database called `event_registration`
- (Optional) Import the `schema.sql` file if you want to set up tables manually, otherwise the application will create them automatically

4. **Set up environment variables**

- Create a `.env` file in the root directory with the following content:
```
# Flask configuration
SECRET_KEY=your-secret-key-here

# Database configuration
DB_USER=root
DB_PASSWORD=your-password-here
DB_HOST=localhost
DB_PORT=3306
DB_NAME=event_registration
```
- Replace `your-secret-key-here` with a secure random string
- Replace `your-password-here` with your MySQL password

5. **Run the application**

```bash
python run.py
```

6. **Access the application**

- The application will be available at http://127.0.0.1:5000/
- Admin login:
  - Username: admin
  - Password: admin123

## Project Structure

```
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── register.html
│   │   ├── admin/
│   │   │   ├── login.html
│   │   │   ├── dashboard.html
│   │   │   ├── add_event.html
│   │   │   ├── edit_event.html
│   │   │   └── registrations.html
│   ├── static/
│   │   └── style.css
│   ├── models.py  
│   ├── routes.py
│   └── __init__.py
├── config.py
├── run.py
├── schema.sql
└── README.md
```

## Troubleshooting

If you encounter database connection issues:

1. Check if XAMPP's MySQL service is running
2. Verify your MySQL username and password in `config.py`
3. Test the database connection by visiting http://127.0.0.1:5000/dbtest
4. Make sure the `event_registration` database exists in MySQL 

## Business Rules

### Event Management
1. Only authenticated administrators can create, edit, or delete events.
2. Events cannot be deleted if they have already started (event date is in the past).
3. Event capacity must be a positive integer.
4. Event title, location, and date are required fields.
5. Events must be scheduled in the future when created.
6. Each event must track which administrator created it.
7. The system maintains the original creator information even if another admin edits the event.

### Registration
1. Users can only register for events that have not yet occurred.
2. Users cannot register for events that have reached their capacity.
3. Each registration requires a unique email address per event.
4. Users must provide last name, first name, email, and phone number to register.
5. A user cannot register multiple times for the same event.
6. Registration is closed once the event has started.
7. Email addresses must be in a valid format (example@domain.com).
8. Phone numbers must follow the format 09xxxxxxxxx (11 digits starting with 09).

### Admin Access
1. Default admin credentials (username: admin, password: admin123) should be changed immediately in production.
2. Only administrators can view the list of registrations for events.
3. Administrators must be authenticated to access the admin dashboard.
4. Failed login attempts should be logged for security purposes.
5. Administrators can view which admin created each event.
6. All sensitive configuration (database credentials, secret keys) is stored in environment variables, not in code.

### Capacity and Attendance
1. The system displays current registration count out of total capacity for each event.
2. Events at full capacity will not allow additional registrations.
3. Registrations are on a first-come, first-served basis.
4. No waitlist functionality is implemented in the current version.
5. Registration counts are displayed in the format "current/total" (e.g., "15/50").

### Data Validation
1. Email addresses must be in a valid format.
2. Phone numbers must be in the format 09xxxxxxxxx.
3. All required fields must be filled before a form can be submitted.
4. Input data is sanitized to prevent SQL injection and XSS attacks.
5. Both client-side and server-side validation are implemented for all forms.
6. School name is optional but provided for outside campus participants.

## Database ERD

![Event Registration System ERD](docs/images/Event%20Registration%20System%20ERD.png) 
