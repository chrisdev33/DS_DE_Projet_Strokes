from helpers import load_config, create_logger
from users import Users


conf = load_config()
logger = create_logger(conf)

users = Users(conf, logger)
print(users.get_user_info('admin'))
print(users.check_user_credentials('admin', '4dm1N'))
