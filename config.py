class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    MY_ENV_VARIABLE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True    
    TOKEN_TTL = 600

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TOKEN_TTL = 86400

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}