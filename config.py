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
    TWILIO_ACCOUNT_SID = 'AC483808afaac154ec873a226270053661'
    TWILIO_AUTH_TOKEN = 'aed5229a82745d9fcc9c33a94d31da70'

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