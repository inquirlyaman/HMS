from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
import configparser
import os.path
HERE = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(HERE, './serviceConfig.ini')

ConfigINI = configparser.ConfigParser()

ConfigINI.read(CONFIG_PATH)
print(ConfigINI.read(CONFIG_PATH))
######## DB settings for serviceConfigS CONFIG ##########
SC_DB_HOST = ConfigINI.get('ServicesConfig', 'DB_HOST')
SC_DB_NAME = ConfigINI.get('ServicesConfig', 'DB_NAME')
SC_DB_USER = ConfigINI.get('ServicesConfig', 'DB_USER')
SC_DB_PASS = ConfigINI.get('ServicesConfig', 'DB_PASS')
services_config_uri = 'postgresql://%s:%s@%s/%s'%(SC_DB_USER, SC_DB_PASS, SC_DB_HOST, SC_DB_NAME)
Engine = create_engine(services_config_uri, convert_unicode=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()
@contextmanager
def session_context():
    """Provide a transactional scope around a series of operations."""
    db_session = Session()
    try:
        yield db_session
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()