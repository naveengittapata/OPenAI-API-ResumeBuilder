import random
import string
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from app.email_service import send_otp_email

auth = Blueprint('auth', __name__)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@auth.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('landing.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not email or not password or not first_name or not last_name:
            flash('All fields are required.', 'error')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('signup.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists.', 'error')
            return render_template('signup.html')

        user = User(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            auth_provider='local'
        )
        user.set_password(password)

        otp = generate_otp()
        user.otp_code = otp
        user.otp_created_at = datetime.utcnow()

        db.session.add(user)
        db.session.commit()

        session['verify_email'] = email
        send_otp_email(email, otp, first_name)

        return redirect(url_for('auth.verify'))

    return render_template('signup.html')

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    email = session.get('verify_email')
    if not email:
        return redirect(url_for('auth.signup'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('auth.signup'))

        if user.otp_code != entered_otp:
            flash('Invalid verification code. Please try again.', 'error')
            return render_template('verify.html', email=email)

        if user.otp_created_at and (datetime.utcnow() - user.otp_created_at) > timedelta(minutes=10):
            flash('Verification code has expired. Please sign up again.', 'error')
            return redirect(url_for('auth.signup'))

        user.is_verified = True
        user.otp_code = None
        user.otp_created_at = None
        db.session.commit()

        session.pop('verify_email', None)
        login_user(user, remember=True)
        flash('Account verified successfully! Welcome!', 'success')
        return redirect(url_for('main.home'))

    return render_template('verify.html', email=email)

@auth.route('/resend-otp', methods=['POST'])
def resend_otp():
    email = session.get('verify_email')
    if not email:
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()
    if user:
        otp = generate_otp()
        user.otp_code = otp
        user.otp_created_at = datetime.utcnow()
        db.session.commit()
        send_otp_email(email, otp, user.first_name)
        flash('A new verification code has been sent to your email.', 'success')

    return redirect(url_for('auth.verify'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        if not user.is_verified:
            session['verify_email'] = email
            otp = generate_otp()
            user.otp_code = otp
            user.otp_created_at = datetime.utcnow()
            db.session.commit()
            send_otp_email(email, otp, user.first_name)
            flash('Please verify your account first. A new code has been sent.', 'error')
            return redirect(url_for('auth.verify'))

        login_user(user, remember=remember)
        return redirect(url_for('main.home'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.landing'))
