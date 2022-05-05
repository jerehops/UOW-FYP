from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from password_strength import PasswordPolicy
from . import db
import re

auth = Blueprint('auth', __name__)

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Invalid Login Details, Please Try Again!')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstname = request.form.get('fName')
    lastname = request.form.get('lName')
    password = request.form.get('password')
    print(check(email))
    if not check(email):
        flash('Invalid email')
        return redirect(url_for('auth.signup'))
    elif not bool(firstname.replace(' ', '').strip() or len(firstname) < 4):
        flash('Invalid First Name')
        return redirect(url_for('auth.signup'))
    elif not bool(lastname.replace(' ', '').strip()) or len(lastname) < 2:
        flash('Invalid Last Name')
        return redirect(url_for('auth.signup'))
    elif not policy.test(password) == []:
        flash("Password not strong enough.")
        return redirect(url_for('auth.signup'))
    else:
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash("User already exists")
            return redirect(url_for('auth.signup'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password, method='sha256'))
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('Account created, please log in')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))