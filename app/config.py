import os

class Config:
    DEBUG = os.getenv("DEBUG", True)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()
