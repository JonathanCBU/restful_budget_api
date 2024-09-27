"""configuration classes for Flask app"""
import os
import dotenv

dotenv.load_dotenv()

class Default:
    TESTING = False
    DEBUG = False
    DATABASE = os.environ["DEMO_DB"]
    DB_SCHEMA = os.environ["DEMO_SCHEMA"]

class Dev(Default):
    DEBUG = True

class Testing(Default):
    TESTING = True
    DATABASE = os.environ["TEST_DB"]