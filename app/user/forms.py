from flask_wtf import FlaskForm
from wtforms import (DateField, RadioField, TextAreaField, SubmitField)
from wtforms.validators import Length
from app.models import User, GenderEnum, PrivacyEnum


## follow/unfollow users
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


## edit user profile information
class EditProfileForm(FlaskForm):
 #   username = StringField('Username', validators=[DataRequired()])
    privacy  = RadioField('Privacy level', choices=PrivacyEnum.to_list())
    gender  = RadioField('Sex ', choices=GenderEnum.to_list())
    about  = TextAreaField('About me', validators=[Length(min=0, max=140)])
    dob  = DateField('Date of Birth', format='%m/%d/%Y')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
