from celery import Celery
# from utils.bzemail import send_mail
# from sbbs import app
from flask import Flask
from flask_mail import Mail,Message
import config

celery_app = Flask('tasks')
celery_app.config.from_object(config)

email = Mail()
email.init_app(celery_app)

celery = Celery('tasks',broker=config.CELERY_BROKER_URL,backend=config.CELERY_RESULT_BACKEND)

def send_mail(subject,receivers,body=None,html=None):
    assert receivers
    if not body and not html:
        return False
    if isinstance(receivers,str) or isinstance(receivers,unicode):
        receivers = [receivers]
    msg = Message(subject=subject,recipients=receivers,body=body,html=html)
    try:
        email.send(msg)
    except:
        return False
    return True

@celery.task
def sendmail(subject,receivers,body=None,html=None):
    with celery_app.app_context():
        send_mail(subject,receivers,body,html)


