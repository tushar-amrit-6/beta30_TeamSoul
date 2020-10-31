import os
import secrets
from app import app
from xray import xray_predict
from flask import render_template, url_for, flash, redirect, request, Response, session
from app.forms import ImageForm, LoginForm

import pyrebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebaseConfig = {
    "apiKey": "AIzaSyD3bIty5_hk-XspqtTASpV2tBlqQyNSPgs",
    "authDomain": "digi-doc-7d829.firebaseapp.com",
    "databaseURL": "https://digi-doc-7d829.firebaseio.com",
    "projectId": "digi-doc-7d829",
    "storageBucket": "digi-doc-7d829.appspot.com",
    "messagingSenderId": "695538257595",
    "appId": "1:695538257595:web:db9a045e63232a3457639e",
    "measurementId": "G-E1E9DPQ022"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/patient/dashboard', methods=['GET', 'POST'])
def patient_dashboard():
    if "user" not in session:
        flash("You must log in first")
        return redirect(url_for("login"))

    form = ImageForm()
    if form.validate_on_submit():
        # covid_prediction = xray_predict(form.picture.data)
        covid_prediction = False
        if covid_prediction is True:
            flash('You have high chances of Covid-19')
        else:
            flash('Congratulations! You have low chances of Covid-19')
    return render_template('patient-dashboard.html', form=form)


@app.route('/patient/family', methods=['GET', 'POST'])
def family():
    return render_template('family.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if "user" in session:
        return redirect(url_for('patient_dashboard'))

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = user
            return redirect(url_for('patient_dashboard'))
        except:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if "user" in session:
        return redirect(url_for('patient_dashboard'))

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('login'))
        except:
            flash('Could not create account')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for('login'))
