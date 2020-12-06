import config

import mysql.connector
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

"""
~$ create database sample_app;
~$ use sample_app;
~$ CREATE TABLE `users` (
  `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(40) DEFAULT '',
  `email` varchar(40) NOT NULL DEFAULT '',
  `password` varchar(200) NOT NULL DEFAULT '',
  `date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


def conn_f():
    _conn = mysql.connector.connect(
        host='localhost', port=3306, user='root', passwd=config.pw, db='sample_app', charset='utf8')
    return _conn


def _is_account_valid(input_email, input_password):
    try:
        conn = conn_f()
        cursor = conn.cursor()
        mysql_cmd = 'select password from users where email="{0}";'.format(
            input_email)
        cursor.execute(mysql_cmd)
        pwd = cursor.fetchone()

        cursor.close()
        conn.close()

        if check_password_hash(pwd[0], input_password):
            print("login successful")
            return True
        else:
            return False
    except:
        print("error")
        return False
