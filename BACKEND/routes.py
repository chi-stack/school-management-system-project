from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from database import db
from models import User, Student

def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

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

def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

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

def edit_student(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        try:
            student.name = request.form['name']
            student.registration_number = request.form['registration_number']
            student.institution = request.form['institution']
            db.session.commit()
            flash('Student updated successfully')
            return redirect(url_for('dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('Registration number already exists. Please use a unique registration number.')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the student.')
    return render_template('edit_student.html', student=student)

def delete_student(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully')
    return redirect(url_for('dashboard'))
