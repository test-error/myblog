from flask import jsonify


class HttpCode:
    ok = 200
    parameserror = 400
    unauth = 401
    methoderror =405
    servererror =500


def json_result(code=HttpCode.ok,message='',data={},kwargs={}):
    json_dict = {'code': code,'message': message,'data': data}
    if kwargs.keys():
        for k,v in kwargs.items():
            data[k] = v
    return jsonify(json_dict)

def json_param_error(message=''):
    return json_result(HttpCode.parameserror,message=message)

def json_unauth_error(message=''):
    return json_result(HttpCode.unauth,message=message)

def json_methoderror_error(message=''):
    return json_result(HttpCode.methoderror,message=message)

def json_servererror_error(message=''):
    return json_result(HttpCode.servererror,message=message)