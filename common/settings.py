import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'SuperSecretKeys'
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
MYSQL_HOSTNAME = os.environ.get('MYSQL_HOSTNAME') or '127.0.0.1'
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME') or 'prod'
MYSQL_DB_NAME = os.environ.get('MYSQL_DB_NAME') or 'mysql-prod'
MYSQLDB_PASSWORD = os.environ.get('MYSQLDB_PASSWORD') or 'welcome1'
MYSQL_PORT = int(os.environ.get('MYSQL_PORT','3306'))
DEBUG = True

if not MYSQL_HOSTNAME:
    logger.error("No MySQL Hostname specified! Exiting!")
    sys.exit()
if not MYSQL_USERNAME:
    logger.error("No MYSQL_USERNAME specified! Exiting!")
    sys.exit()
if not MYSQL_DB_NAME:
    logger.error("No MYSQL_DB_NAME specified! Exiting!")
    sys.exit()
if not MYSQLDB_PASSWORD:
    logger.error("No MYSQLDB_PASSWORD specified! Exiting!")
    sys.exit()
