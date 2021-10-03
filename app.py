from flask import Flask

from api.auth import auth
from api.news import news
from api_response import APIResponse

from database import init_db, db_session
from models import User, News, NewsImage

app = Flask(__name__)
app.response_class = APIResponse

app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(news, url_prefix='/api')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin12345@localhost:3306/appd'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db()

# db_session.add(User('kek', 'dsfsdfs@dsfsd.dsfsd', '123456'))
# db_session.add(News('fsfsd', 'fsdfsdf', 1))
# db_session.add(NewsImage(1, 'fdsfsfs'))
# db_session.add(NewsImage(1, 'vcxvxvx'))
# db_session.commit()

if __name__ == '__main__':
    # database.db_session.create_all()
    app.run(debug=True)
