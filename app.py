from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zie_regulatory_system_2026"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost:5432/zie_registration_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'zie_users_classic'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    full_name = db.Column(db.String(200))
    role = db.Column(db.String(20), default='applicant')
    origin = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register/<origin_type>', methods=['GET', 'POST'])
def register(origin_type):
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        password = request.form['password']

        user = User(username=username, full_name=full_name, password=password, origin=origin_type)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', origin_type=origin_type)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(debug=True)