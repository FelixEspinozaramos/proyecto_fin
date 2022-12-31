class config:
    DEBUG = True
    TEXTING = True

    #configuracion
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:ramos11@localhost:3306/final"

class ProductionConfig(config):
    DEBUG = False

class DevelopmentConfig(config):
    SECRET_KEY = 'dev'
    DEBUG = True
    TEXTING = True


