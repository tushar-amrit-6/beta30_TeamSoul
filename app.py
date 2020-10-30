from flask import Flask, render_template

# Flask Config:
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/patient/dashboard')
def patient_dashboard():
    return render_template('patient-dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
