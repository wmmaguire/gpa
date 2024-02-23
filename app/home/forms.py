#!/usr/bin/env python
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField


## form to search for group
class SearchForm(FlaskForm):
    choices = [('User', 'User')]
    select = SelectField('Categories', choices=choices)
    search = StringField('')
    submit = SubmitField('Search')
