# Deploying to PythonAnywhere

This guide explains how to deploy the Event Registration System on PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (free tier is sufficient for basic usage)
2. Your application code (either uploaded or cloned from a Git repository)

## Step 1: Create a PythonAnywhere Account

If you don't have one already, sign up at [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/).

## Step 2: Upload Your Code

You have two options:

### Option 1: Upload a ZIP file
1. Compress your entire project folder (excluding virtual environment if you have one)
2. In PythonAnywhere, go to the "Files" tab
3. Click "Upload a file" and select your ZIP file
4. Once uploaded, use the "Open Bash console here" button to open a console
5. Unzip your project: `unzip your-project.zip`

### Option 2: Clone from Git
1. In PythonAnywhere, go to the "Consoles" tab and start a new Bash console
2. Navigate to where you want to store your project: `cd ~`
3. Clone your repository: `git clone https://github.com/yourusername/your-repository.git`

## Step 3: Set Up a Virtual Environment

1. In your Bash console, navigate to your project directory:
   ```bash
   cd ~/your-project-directory
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install your dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Set Up MySQL Database

1. Go to the "Databases" tab in PythonAnywhere
2. Set a MySQL password if you haven't already
3. Create a new database called `event_registration`
4. Note your MySQL username (usually the same as your PythonAnywhere username)

## Step 5: Configure Environment Variables

1. Create/update your `.env` file in your project directory:
   ```bash
   nano .env
   ```

2. Add the following configurations (adjust as needed):
   ```
   SECRET_KEY=your-secret-key-here
   DB_USER=your-pythonanywhere-username
   DB_PASSWORD=your-mysql-password
   DB_HOST=your-pythonanywhere-username.mysql.pythonanywhere-services.com
   DB_PORT=3306
   DB_NAME=event_registration
   ```

3. Save and exit (Ctrl+X, then Y, then Enter)

## Step 6: Set Up a Web App

1. Go to the "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Select "Manual configuration" (not the Flask option)
4. Select Python version (3.8 or higher recommended)

## Step 7: Configure the Web App

1. In the "Code" section:
   - Set "Source code" to your project directory (e.g., `/home/yourusername/your-project-directory`)
   - Set "Working directory" to the same path

2. In the "Virtualenv" section:
   - Enter the path to your virtual environment (e.g., `/home/yourusername/your-project-directory/venv`)

3. In the "WSGI configuration file" section:
   - Click the link to edit the WSGI file
   - Replace the content with the following (adjust paths as needed):

   ```python
   import sys
   import os
   from dotenv import load_dotenv

   # Add your project directory to the Python path
   path = '/home/yourusername/your-project-directory'
   if path not in sys.path:
       sys.path.append(path)

   # Load environment variables
   load_dotenv(os.path.join(path, '.env'))

   # Import your Flask app
   from run import app as application
   ```

4. Save the WSGI file

## Step 8: Set Up Static Files

1. In the "Static files" section of your web app:
   - Add an entry with:
     - URL: `/static/`
     - Directory: `/home/yourusername/your-project-directory/app/static`

## Step 9: Initialize the Database

1. Go to the "Consoles" tab and start a new Bash console
2. Navigate to your project directory and activate your virtual environment:
   ```bash
   cd ~/your-project-directory
   source venv/bin/activate
   ```

3. Open a Python console:
   ```bash
   python
   ```

4. Initialize your database:
   ```python
   from app import create_app, db
   from app.models import Admin
   from werkzeug.security import generate_password_hash
   
   app = create_app()
   with app.app_context():
       db.create_all()
       
       # Check if admin user exists
       admin = Admin.query.filter_by(username='admin').first()
       if not admin:
           admin = Admin(username='admin')
           admin.password_hash = generate_password_hash('admin123')
           db.session.add(admin)
           db.session.commit()
           print("Default admin user created!")
   
   exit()
   ```

## Step 10: Reload Your Web App

1. Go back to the "Web" tab
2. Click the green "Reload" button for your web app

Your Event Registration System should now be deployed and accessible at `yourusername.pythonanywhere.com`.

## Important Security Notes

1. Change the default admin password immediately after first login
2. Use a strong, unique SECRET_KEY
3. Consider using HTTPS (available on paid PythonAnywhere accounts)
4. Regularly backup your database

## Troubleshooting

If your app doesn't work, check:
1. The error log in the "Web" tab
2. Database connection settings in your `.env` file
3. File permissions
4. WSGI configuration

For more help, visit the [PythonAnywhere help pages](https://help.pythonanywhere.com/). 