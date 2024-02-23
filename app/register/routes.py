from flask import (render_template, flash, redirect, url_for)
from flask_login import current_user
from . import blueprint
from .forms import UserRegistrationForm
from app.models import User
from app import db


## register user account
@blueprint.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('user_blueprint.user', current_user.username))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth_blueprint.login'))
    return render_template('register.html', title='User Registration', form=form)
