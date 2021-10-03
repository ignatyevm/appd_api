from flask import request, Blueprint

from api_response import APIError, APIResponse
from models import News
from validator import FieldValidator, ValidationError, validate
from database import db_session, redis_session

news = Blueprint('news', __name__)


@news.route('/news.get', methods=['POST'])
def get_news():
    news_list = []
    for news in News.query.all():
        news_list.append({
            'title': news.title,
            'description': news.description,
            'images': [image.url for image in news.images],
            'author': {
                'id': news.author.id,
                'name': news.author.name
            },
            'date': news.date
        })
    return APIResponse({'news': news_list})


@news.route('/news.create', methods=['POST'])
def create_news():
    params = request.form
    validators = [
        FieldValidator('title').required().string().max_len(255),
        FieldValidator('description').required().string(),
        FieldValidator('access_token').required()
    ]
    values, errors = validate(params, validators)
    if len(errors) > 0:
        return APIError(errors)
    title, description, access_token = values
