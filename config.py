from os import environ, path
#from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask config variables."""

    #FLASK_ENV = environ.get('FLASK_ENV')
    #TESTING = environ.get('TESTING_MODE')
    DEBUG = True
    
    
    # Database
    #DB_USER = environ.get('DB_USER')
    #DB_PASSWORD = environ.get('DB_PASSWORD')
    #DB_NAME = environ.get('DB_NAME')

    
   
    
    

