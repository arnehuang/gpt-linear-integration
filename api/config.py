import os


class Config:
    """
    Base Configuration
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "testkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"  # where logs are outputted to
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "DATABASE_URL_NOT_SET")
    SQLALCHEMY_POOL_RECYCLE = 150  # recycle connection after 150 seconds
    SQLALCHEMY_POOL_TIMEOUT = 60  # timeout after 60 seconds
    SQLALCHEMY_PRE_PING = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
        "pool_timeout": SQLALCHEMY_POOL_TIMEOUT,
        "pool_pre_ping": SQLALCHEMY_PRE_PING,
    }


class DevelopmentConfig(Config):
    """
    Development Configuration - default config
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production Configuration
    Requires the environment variable `FLASK_ENV=prod`
    """

    DEBUG = False


# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig, "prod": ProductionConfig}
