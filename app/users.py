import os

from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError


class Users:
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger

        self.mysql_host = str(os.getenv('MYSQL_HOST'))
        self.mysql_port = str(os.getenv('MYSQL_PORT'))
        self.mysql_url = self.mysql_host + ':' + self.mysql_port
        self.mysql_dbname = os.getenv('MYSQL_DATABASE')
        self.mysql_user = os.getenv('MYSQL_ROOT_USER')
        self.mysql_password = os.getenv('MYSQL_ROOT_PASSWORD')
        self.encrypt_key = os.getenv('MYSQL_ENCRYPT_KEY')

        # self.mysql_host = 'localhost'
        # self.mysql_port = '3306'
        # self.mysql_url = self.mysql_host + ':' + self.mysql_port
        # self.mysql_dbname = 'strokes'
        # self.mysql_user = 'root'
        # self.mysql_password = 'datascientest1234'
        # self.encrypt_key = 'strokes'

        # recreating the URL connection
        self.my_connection_url = 'mysql+mysqlconnector://{user}:{password}@{url}/{database}'.format(
            user=self.mysql_user,
            password=self.mysql_password,
            url=self.mysql_url,
            database=self.mysql_dbname
        )

        try:
            self.mysql_engine = create_engine(self.my_connection_url)
        
        except SQLAlchemyError as err:
            self.logger.error(err)


    def verify_username_password(self, name: str, password: str):
        try:
            mysql_connection = self.mysql_engine.connect()
            with mysql_connection:
                sql = '''SELECT user_id, user_name, user_role
                           FROM users 
                          WHERE user_name = :x
                            AND AES_DECRYPT(user_password, :z) = :y'''
                sql = text(sql)
                result = mysql_connection.execute(sql, x=name, y=password, z=self.encrypt_key).fetchall()
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