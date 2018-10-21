import os

import requests
from awsauth import S3Auth

import config

with open(os.path.expanduser("~/.boto")) as f:
  lines = f.read().splitlines()
ACCESS_KEY = lines[1].split(' = ')[1]
SECRET_KEY = lines[2].split(' = ')[1]

USERNAME = config.config_dict.get('username')

bucket_name = 'jca-screenshots-{}-normal'.format(USERNAME)
url = 'http://{}.s3.amazonaws.com?prefix=2018-01-19'.format(bucket_name)

resp = requests.get(url, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
print 'status:', resp.status_code
print 'content:', resp.content
