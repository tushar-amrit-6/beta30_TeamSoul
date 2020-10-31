import os
import secrets
import random
from app import app
from xray import model_predict
from flask import render_template, url_for, flash, redirect, request, Response, session
from app.forms import ImageForm, LoginForm, SignupForm, AddMemberForm, DetailsForm
from flask_mysqldb import MySQL
import MySQLdb.cursors


app.config['SECRET_KEY'] = 'TeamBeta30'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12373645'
app.config['MYSQL_PASSWORD'] = 'J7i89uAyM8'
app.config['MYSQL_DB'] = 'sql12373645'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/assets/img/xray', picture_name)

    form_picture.save(picture_path)
    return picture_name


@app.route('/patient/dashboard', methods=['GET', 'POST'])
def patient_dashboard():
    if "email" not in session:
        flash("You must log in first")
        return redirect(url_for("login"))

    form = ImageForm()
    if form.validate_on_submit():
        f_name = save_picture(form.picture.data)
        covid_prediction = model_predict(os.path.join(
            app.root_path, 'static/assets/img/xray', f_name), )
        if covid_prediction is True:
            flash('You have high chances of Covid-19')
        else:
            flash('Congratulations! You have low chances of Covid-19')
    return render_template('patient-dashboard.html', form=form)


@app.route('/patient/profile', methods=['GET', 'POST'])
def profile():
    form = DetailsForm()
    if request.method == "POST":
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        bloodgrp = request.form["bloodgrp"]

        email = session["email"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'UPDATE DETAILS SET age = %s, height = %s,weight = %s,blood_grp = %s WHERE email = %s', (age, height, weight, bloodgrp, email))
        mysql.connection.commit()
        return redirect(url_for('patient_dashboard'))
    return render_template('profile.html', form=form)


@app.route('/patient/family', methods=['GET', 'POST'])
def family():
    form = AddMemberForm()
    if "email" in session and request.method == "GET":
        email = session['email']
        fid = session['fid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM DETAILS WHERE familyid = %s', (fid,))
        members = cursor.fetchall()
        return render_template('family.html', members=members, form=form)

    elif "email" in session and request.method == "POST":
        if "new_email" in request.form and request.method == "POST":
            cur_email = session['email']
            cur_fid = session['fid']
            new_email = request.form['new_email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT familyid FROM DETAILS WHERE email = %s', (new_email,))
            member = cursor.fetchone()
            if member:
                new_fid = member['familyid']
                cursor.execute(
                    'UPDATE USERS SET familyid = %s WHERE familyid = %s', (cur_fid, new_fid))
                mysql.connection.commit()
                cursor.execute(
                    'UPDATE DETAILS SET familyid = %s WHERE familyid = %s', (cur_fid, new_fid))
                mysql.connection.commit()
            else:
                flash("No such User!")
        return redirect(url_for('family'))
    else:
        return redirect(url_for('login'))


@app.route('/doctor')
def doctor():
    if "email" in session and request.method == "GET":
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM DETAILS WHERE email NOT IN ("sosinesta3@gmail.com")')
        members = cursor.fetchall()
        return render_template('doctor.html', members=members)

    return render_template('doctor.html')


@app.route('/pharmacy')
def pharmacy():
    return render_template('pharmacy.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if "email" in session:
        return redirect(url_for('patient_dashboard'))

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM USERS WHERE email = %s AND password = %s', (email, password))
        patient = cursor.fetchone()
        if patient:
            session['loggedin'] = True
            session['email'] = patient['email']
            cursor.execute(
                'SELECT * FROM USERS WHERE email = %s', (email,))
            patient = cursor.fetchone()
            session['fid'] = patient["familyid"]

            if session["email"] == 'sosinesta3@gmail.com':
                return redirect(url_for('doctor'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if "email" in session:
        return redirect(url_for('profile'))

    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USERS WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            flash('Email already Exists!')
        else:
            fid = random.randint(1, 9999)
            cursor.execute(
                '''INSERT INTO USERS VALUES (%s, %s, %s,%s,'1234567890',-1,-1,-1,'NA')''', (name, email, password, fid))
            cursor.execute(
                '''INSERT INTO DETAILS VALUES (%s,'NA',-1,%s,'1234567890',-1,-1,-1,'NA','NA','NA')''', (email, fid))
            mysql.connection.commit()
            flash('You have succesfully registered!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for('login'))
