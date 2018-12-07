from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import common.settings as cfg
from common.logging_module import get_logger
import sys
import datetime
import uuid

logger = get_logger('user')

class UserModel:
    def __init__(self, uid, first_name, email_id, password, last_login):
        self.id = uid
        self.username = email_id
        self.password = password
        self.last_login = last_login
        self.name = first_name
        print (self.username + ' and '  + self.password)

    @classmethod
    def find_by_username(cls, username):
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            sys.exit()
        cursor = db.cursor()
        query = "select user_uid,first_name,email_id,password,last_login from corp_tenancy_user_tab where email_id=%s"
        cursor.execute(query,(username,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        db.close
        return user

    @classmethod
    def find_by_id(cls, _id):
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            sys.exit()
        cursor = db.cursor()
        query = "select user_uid,first_name,email_id,password,last_login from corp_tenancy_user_tab where user_uid=%s"
        cursor.execute(query,(_id,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        db.close
        return user
