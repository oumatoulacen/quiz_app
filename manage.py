from app import create_app
from config import Config


# # Config example: in config.py file create a class Config: and add the following code with your secret key and database URI
# class Config:
#     SECRET_KEY = 'your secret key'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/quiz_app'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


app = create_app(Config)

if __name__ == '__main__':
    app.run()
