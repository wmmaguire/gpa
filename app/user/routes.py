#!/usr/bin/env python
from . import blueprint
from .forms import EditProfileForm, EmptyForm
from flask import (request, render_template, flash, redirect, url_for)
from flask_login import (current_user, login_required)
from app.models import User
from app import db

## profile page
@blueprint.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, form = EmptyForm())


## profile editor
@blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.privacy = form.privacy.data
        current_user.gender = form.gender.data
        current_user.about = form.about.data
        current_user.dob = form.dob.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user_blueprint.user', username=current_user.username))
    elif request.method == 'GET':
        form.privacy.data = current_user.privacy
        form.gender.data = current_user.gender
        form.about.data = current_user.about
        form.dob.data = current_user.dob

    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
# ajax callbacks

## display userdata in popup window
@blueprint.route('/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)
