"""configuration classes for Flask app"""
import os
import dotenv

dotenv.load_dotenv()

class Default:
    TESTING = False
    DEBUG = False
    DATABASE = os.environ["DEMO_DB"]

class Dev(Default):
    DEBUG = True