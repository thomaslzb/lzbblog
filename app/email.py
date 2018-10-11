from flask_mail import Message
from threading import Thread
from flask import current_app
from app import mail

def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    if sync:
        nail.send(msg)
    else:
        # asynchronous send mail
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_async_email(current_app, msg):
    with current_app.app_context():
        #these contexts are automatically managed by the framework
        mail.send(msg)



