from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import TextAreaField, SubmitField
from flask_babel import lazy_gettext as _l
from wtforms.validators import ValidationError, DataRequired,  EqualTo, Length
from app.models import User
from flask import request

class EditPorfileForm(FlaskForm):
    username = StringField(_l('username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('about_me'), validators= [Length(min=0,max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditPorfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something:'), validators=
        [DataRequired(), Length(min=1, max =140)])
    submit = SubmitField(_l('Submit'))

def _required(form, field):
    """ This function to check validators is null for "Cancle" button """
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField(_l('Original Password'), validators=[_required])
    password = PasswordField(_l('New Password'), validators=[_required])
    password2 = PasswordField(_l('Confirm New Password'), validators=[_required, EqualTo('password')])
    submitconfirm = SubmitField(_l('Confirm Change'))
    submitcancle = SubmitField(_l('Cancle'))


class Searchform(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled'  not in kwargs:
            kwargs['csrf_enabled'] = False
        super(Searchform, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'),  validators=
        [DataRequired(), Length(min=0,max=150)])
    submit = SubmitField(_l('Submit'))



