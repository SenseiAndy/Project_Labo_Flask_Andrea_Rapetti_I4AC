from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from models.model import *
from flask import url_for
from flask import flash
from models.model import User
from flask_login import *

app = Blueprint('auth', __name__)

@app.route('/login')
def login():
    # return the login form
    
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('auth.profile'))
    return render_template('/auth/login.html')


@app.route('/login', methods=['POST'])
def login_post():
    

    email = request.form.get('email')
    password = request.form.get('password')

    stmt = db.select(User).filter_by(email=email)
    user = db.session.execute(stmt).scalar_one_or_none()
    

    if user:
        if user.check_password(password):
            login_user(user)
            return redirect(url_for('auth.profile'))
        else:
            flash('Invalid password! Try again.')
            return redirect(url_for('auth.login'))
    else:
        flash('Invalid account.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    


@app.route('/logout')
@login_required
def logout():
   
    username = current_user.username
    logout_user()
    return render_template('/auth/logout.html', name=username)
    return render_template('/logout.html')


@app.route('/profile')
@login_required
def profile():
   
    return render_template('/auth/profile.html', name=current_user.username, email=current_user.email, id=current_user.id)