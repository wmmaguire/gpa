from flask import render_template
from flask_mail import Message
from flask import current_app
from app import mail
from threading import Thread

## send email task
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

## send eemail in threaded task
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args = (current_app, msg)).start()

## send password reset email
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Personal Fitness] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
