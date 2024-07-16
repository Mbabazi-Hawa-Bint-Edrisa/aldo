class Config:
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost/aldo_safaris"
    JWT_SECRET_KEY='safaris'
# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://username:password@localhost/project2')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False



