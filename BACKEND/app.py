from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import os
from database import db
from flask_cors import CORS
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(__file__), "instance", "students.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Import models after db is defined
from models import User, Student

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    search = request.args.get('search', '')
    if search:
        students = Student.query.filter(
            (Student.name.contains(search)) |
            (Student.registration_number.contains(search)) |
            (Student.institution.contains(search))
        ).all()
    else:
        students = Student.query.all()
    return render_template('dashboard.html', students=students, search=search)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        registration_number = request.form['registration_number']
        institution = request.form['institution']
        try:
            new_student = Student(name=name, registration_number=registration_number, institution=institution)
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully')
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('Registration number already exists. Please use a unique registration number.')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the student.')
    return render_template('add_student.html')

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.registration_number = request.form['registration_number']
        student.institution = request.form['institution']
        db.session.commit()
        flash('Student updated successfully')
        return redirect(url_for('dashboard'))
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully')
    return redirect(url_for('dashboard'))

# API Routes
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'})

@app.route('/api/students', methods=['GET'])
def api_students():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    search = request.args.get('search', '')
    if search:
        students = Student.query.filter(
            (Student.name.contains(search)) |
            (Student.registration_number.contains(search)) |
            (Student.institution.contains(search))
        ).all()
    else:
        students = Student.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'registration_number': s.registration_number,
        'institution': s.institution
    } for s in students])

@app.route('/api/students', methods=['POST'])
def api_add_student():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    name = data.get('name')
    registration_number = data.get('registration_number')
    institution = data.get('institution')
    try:
        new_student = Student(name=name, registration_number=registration_number, institution=institution)
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student added successfully', 'id': new_student.id})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Registration number already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred'}), 500

@app.route('/api/students/<int:id>', methods=['PUT'])
def api_edit_student(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    student = Student.query.get_or_404(id)
    data = request.get_json()
    student.name = data.get('name', student.name)
    student.registration_number = data.get('registration_number', student.registration_number)
    student.institution = data.get('institution', student.institution)
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

@app.route('/api/students/<int:id>', methods=['DELETE'])
def api_delete_student(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            hashed_password = generate_password_hash('admin123')
            admin = User(username='admin', password=hashed_password)
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
