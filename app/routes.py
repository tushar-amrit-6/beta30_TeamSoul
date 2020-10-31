import os
import secrets
from app import app
from xray import model_predict
from flask import render_template, url_for, flash, redirect, request, Response, session
from app.forms import ImageForm, LoginForm


@app.route('/')
def home():
    return render_template('home.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/assets/img/xray', picture_name)

    form_picture.save(picture_path)
    return picture_name


@app.route('/patient/dashboard', methods=['GET', 'POST'])
def patient_dashboard():
    # if "user" not in session:
    # flash("You must log in first")
    # return redirect(url_for("login"))

    form = ImageForm()
    if form.validate_on_submit():
        f_name = save_picture(form.picture.data)
        covid_prediction = model_predict('/static/assets/img/xray/0110c76a1cbc5366.jpeg')
        if covid_prediction is True:
            flash('You have high chances of Covid-19')
        else:
            flash('Congratulations! You have low chances of Covid-19')
    return render_template('patient-dashboard.html', form=form)


@app.route('/patient/family', methods=['GET', 'POST'])
def pharmacy():
    return render_template('family.html')

@app.route('/pharmacy', methods=['GET'])
def family():
    return render_template('pharmacy.html')


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
