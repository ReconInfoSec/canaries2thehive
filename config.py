import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HIVE_URL='http://localhost:9000'
    LOG_FILE='/var/log/canaries2thehive.log'
