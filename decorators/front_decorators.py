from functools import wraps
import constants
from flask import session,abort

def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        frontuser_id = session.get(constants.FRONTUSER_SESSION_ID)
        if not frontuser_id:
            return func(*args,**kwargs)
        else:
            abort(401)
    return wrapper