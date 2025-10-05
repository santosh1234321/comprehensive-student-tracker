# Student Performance Management System
This is a simple web application built with Flask and SQLite to manage student academic performance. It allows users to add, view, update, and delete student records with scores in Math, Science, and English, while automatically calculating total marks, average score, and letter grade.

## Features
- Add new student records with scores in three subjects
- View all students' details with calculated total, average, and grade
- Edit scores for existing students with recalculated metrics
- Delete student records
- Uses SQLite for lightweight, file-based storage
- Responsive and intuitive web interface with Flask templates

## Technologies Used
- Flask: Web framework for Python
- SQLite: Embedded relational database engine
- Jinja2: Templating engine used by Flask
- HTML/CSS: Frontend structure and styling
- Python: Backend logic and database management

## Installation & Usage
- Clone the repository
- Install Flask if not already installed:
bash
pip install flask
- Run the app:
bash
python app.py
Open your browser to http://127.0.0.1:5000/
- Use the web interface to manage student records

## Code Structure
- app.py: Main Flask application containing routes and database connection logic
- student_performance.db: SQLite database file (created on app first run)

templates/: Folder with HTML templates for listing, adding, and editing students

Student class: Handles score calculations including total, average, and grade assignment
