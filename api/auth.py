import random

from flask import request, Blueprint

from api_response import APIError, APIResponse
from models import User
from validator import FieldValidator, ValidationError, validate
import errors_codes
from database import db_session, redis_session

auth = Blueprint('auth', __name__)


def generate_access_token():
    import secrets
    return secrets.token_hex(64)


def hash_password(password):
    import hashlib
    salt = 'ew832ejeWdSI21E23esdf231eq'
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


@auth.route('/auth.register', methods=['POST'])
def register():
    params = request.form
    validators = [
        FieldValidator('name').required().string().max_len(255),
        FieldValidator('email').required().string().max_len(255).email(),
        FieldValidator('password').required().string().min_len(6).max_len(255),
    ]
    values, errors = validate(params, validators)
    if len(errors) > 0:
        return APIError(errors)
    name, email, password = values
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return APIError([{
            'error_code': errors_codes.used_email
        }])

    code = random.randint(111111, 999999)

    print('code: ', code)

    redis_session.hmset(email, {'name': name, 'password': password, 'code': code})
    redis_session.expire(email, 10 * 60)

    return APIResponse()


@auth.route('/auth.verify_email', methods=['POST'])
def verify_email():
    params = request.form
    validators = [
        FieldValidator('email').required().string().max_len(255),
        FieldValidator('code').required().string()
    ]
    values, errors = validate(params, validators)
    if len(errors) > 0:
        return APIError(errors)

    email, code = values

    if not redis_session.exists(email):
        return APIError({'error_code': errors_codes.used_email})

    name, password, actual_code = redis_session.hgetall(email).values()

    if code != actual_code:
        return APIError({'error_code': errors_codes.wrong_verification})

    redis_session.delete(email)

    db_session.add(User(name, email, hash_password(password)))
    db_session.commit()

    access_token = generate_access_token()
    redis_session.setex(email, 60 * 60 * 24 * 30, access_token)

    return APIResponse({'access_token': access_token})


@auth.route('/auth.login', methods=['POST'])
def login():
    params = request.form
    validators = [
        FieldValidator('email').required().string().max_len(255),
        FieldValidator('password').required().string().min_len(6).max_len(255),
    ]

    values, errors = validate(params, validators)
    if len(errors) > 0:
        return APIError(errors)

    email = values[0]
    password = hash_password(values[1])

    user = User.query.filter_by(email=email).first()

    if user is None or password != user.password:
        return APIError({'error_code': errors_codes.wrong_creditionals})

    access_token = None
    if redis_session.exists(email):
        access_token = redis_session.get(email)
    else:
        access_token = generate_access_token()
        redis_session.setex(email, 60 * 60 * 24 * 30, access_token)

    return APIResponse({'access_token': access_token})
