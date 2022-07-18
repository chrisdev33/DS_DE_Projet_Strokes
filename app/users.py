import os

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


class Users:
    def __init__(self, conf, logger, mysql_engine, mysql_encrypt_key):
        self.conf = conf
        self.logger = logger
        self.mysql_engine = mysql_engine
        self.mysql_encrypt_key = mysql_encrypt_key

    def verify_username_password(self, name: str, password: str):
        try:
            mysql_connection = self.mysql_engine.connect()
            with mysql_connection:
                sql = '''SELECT user_id, user_name, user_role
                           FROM users 
                          WHERE user_name = :x
                            AND AES_DECRYPT(user_password, :z) = :y'''
                sql = text(sql)
                result = mysql_connection.execute(sql, x=name, y=password, z=self.mysql_encrypt_key).fetchall()
                return len(result)
        
        except SQLAlchemyError as err:
            self.logger.error(err)


    def get_user_info(self, name: str):
        try:
            mysql_connection = self.mysql_engine.connect()
            with mysql_connection:
                sql = '''SELECT user_id, user_name, user_role
                           FROM users 
                          WHERE user_name = :x'''
                sql = text(sql)
                result = mysql_connection.execute(sql, x=name).fetchall()
                return result

        except SQLAlchemyError as err:
            self.logger.error(err)