from flask import (request, render_template, flash, redirect, url_for)
from flask_login import (current_user, login_user, logout_user)
from . import blueprint
from .forms import (LoginForm, ResetPasswordRequestForm, ResetPasswordForm)
from werkzeug.urls import url_parse
from app import db 
from app.models import User
from app.email import send_password_reset_email

## login page 
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_blueprint.user', username = current_user.username))
    form = LoginForm()
    # evaluate user credentials
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # bad credentials
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth_blueprint.login'))
        # login user and perform proper redirect
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user_blueprint.user', username =  current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

## request password page (sends email)
@blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth_blueprint.login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

## reset password page (send email)
@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home_blueprint.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth_blueprint.login'))
    return render_template('reset_password.html', form=form)

## logout redirect
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.index'))
