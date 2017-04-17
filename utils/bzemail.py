# from exts import email

from flask_mail import Message
from tasks import email

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
