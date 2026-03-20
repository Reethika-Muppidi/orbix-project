from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, User
from config import Config
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.config.from_object(Config)

# ---------------- DB ----------------
db.init_app(app)

# ---------------- LOGIN ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- ROOT ----------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ---------------- HOME ----------------
@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))

        flash("Invalid email or password", "danger")

    return render_template('login.html')

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ---------------- INCOME ----------------
@app.route('/income')
@login_required
def income():
    data = {
        "name": current_user.name,
        "total_items": random.randint(15, 30),
        "delivered": random.randint(5, 15),
        "external_factors": random.choice([
            "Rain delay 🌧️",
            "Heavy traffic 🚗",
            "Bike issue 🔧",
            "No issues ✅"
        ]),
        "weekly_premium": random.randint(10, 50),
        "location": random.choice([
            "Hyderabad",
            "Bangalore",
            "Chennai",
            "Delhi"
        ])
    }

    data["pending"] = data["total_items"] - data["delivered"]

    return render_template('income.html', data=data)

# ---------------- NOTIFICATIONS ----------------
@app.route('/notifications')
@login_required
def notifications():
    delivery_ids = [random.randint(100, 999) for _ in range(5)]
    return render_template('notifications.html', delivery_ids=delivery_ids)

# ---------------- ABOUT ----------------
@app.route('/about')
@login_required
def about():
    return render_template('about.html')

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)