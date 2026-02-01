# Student E-Records Management System

## Description
A web-based application for managing student records, built with Flask and SQLite. It provides a simple interface for administrators to add, view, edit, and delete student information.

## Problem Statement
Educational institutions need an efficient way to manage student records digitally. This system provides a secure, user-friendly platform for administrators to maintain student data.

## Technologies Used
- **Backend:** Flask (Python web framework)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Werkzeug for password hashing

## Features
- Admin authentication system
- CRUD operations for student records (Create, Read, Update, Delete)
- Search functionality across student data
- Responsive Bootstrap UI
- Error handling for database operations
- Flash messages for user feedback

## Installation Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Steps
1. Clone or download the project files
2. Navigate to the `PROJECT/BACKEND` directory
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```PS C:\Users\PC\Desktop\PROJECT> start http://127.0.0.1:5000/
PS C:\Users\PC\Desktop\PROJECT> 


5. Open your web browser and go to `http://127.0.0.1:5000/`

## Login Credentials
- **Username:** admin
- **Password:** admin123

## Project Structure
```
PROJECT/
├── BACKEND/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── routes.py           # Route handlers
│   ├── database.py         # Database configuration
│   ├── requirements.txt    # Python dependencies
│   └── templates/          # HTML templates
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── add_student.html
│       └── edit_student.html
└── README.md
```

## Usage
1. Login with the provided admin credentials
2. View the dashboard with existing student records
3. Add new students using the "Add New Student" button
4. Edit or delete existing records using the action buttons
5. Use the search bar to filter students by name, registration number, or institution

## Contributing
Feel free to fork this project and submit pull requests for improvements.

## License
This project is open source and available under the MIT License.
