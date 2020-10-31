import os
import secrets
from app import app
from xray import xray_predict
from flask import render_template, url_for, flash, redirect, request, Response
from app.forms import ImageForm, LoginForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/patient/dashboard', methods=['GET', 'POST'])
def patient_dashboard():
    form = ImageForm()
    if form.validate_on_submit():
        # covid_prediction = xray_predict(form.picture.data)
        covid_prediction = False
        if covid_prediction is True:
            flash('You have high chances of Covid-19')
        else:
            flash('Congratulations! You have low chances of Covid-19')
    return render_template('patient-dashboard.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
