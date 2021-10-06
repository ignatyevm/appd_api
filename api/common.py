import jwt
import config


def encode_jwt(user):
    return jwt.encode({'user': {
        'id': user.id,
        'name': user.name,
        'role': user.role
    }}, config.secret_key)


def decode_jwt(token):
    payload = jwt.decode(token, config.secret_key, ['HS256'])
    return [payload['user'][key] for key in ['id', 'name', 'role']]
