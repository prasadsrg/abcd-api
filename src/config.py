class Config(object):
    """
    Common configurations
    """
    HOST = '0.0.0.0'
    PORT = 2001
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Admin!234@localhost/abcd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Put any configurations here that are common across all environments


class QaConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


app_config = {
    'DEV': DevelopmentConfig,
    'QA': QaConfig,
    'PRD': ProductionConfig
}
