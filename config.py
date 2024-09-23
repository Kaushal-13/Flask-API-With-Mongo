import os


class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
