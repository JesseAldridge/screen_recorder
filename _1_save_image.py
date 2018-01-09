import os, sys, subprocess, resource, time, threading
from datetime import datetime

import requests
from awsauth import S3Auth

import _0_mem_logger
import config

if sys.platform == 'darwin':
  import _0_os_osx as os_specific
elif _platform == 'win32':
  import _0_os_windows as os_specific
else:
  print 'Unsupported OS'
  sys.exit()

with open(os.path.expanduser("~/.boto")) as f:
  lines = f.read().splitlines()
ACCESS_KEY = lines[1].split(' = ')[1]
SECRET_KEY = lines[2].split(' = ')[1]

USERNAME = config.config_dict.get('username', 5)

screens_path = os.path.expanduser(os.path.join('~', 'screenshots'))

def init_dirs():
  ' Create directories if needed. '

  if not os.path.exists(screens_path):
    os.mkdir(screens_path)

  thumb_dir = os.path.join(screens_path, 'thumbnails')
  if not os.path.exists(thumb_dir):
    os.mkdir(thumb_dir)

  webcam_dir = os.path.join(screens_path, 'webcam')
  if not os.path.exists(webcam_dir):
    os.mkdir(webcam_dir)

  return screens_path, thumb_dir, webcam_dir

def save_image(temp_file, final_path, is_thumb=False):
  ' Save the img.  Scale down thumbnails. '

  scale = .05 if is_thumb else .5

  image_dims = 'x'.join([str(int(x * scale)) for x in os_specific.get_screen_size()])
  proc = subprocess.Popen(
    ['/usr/local/bin/convert', temp_file.name, '-resize', image_dims, final_path])
  timer = threading.Timer(3, lambda p: p.kill(), [proc])
  try:
    timer.start()
    proc.communicate()
  finally:
    timer.cancel()

  bucket_type = 'thumbs' if is_thumb else 'normal'
  bucket_name = 'jca-screenshots-{}-{}'.format(USERNAME, bucket_type)
  filename = os.path.basename(final_path)
  url = 'http://{}.s3.amazonaws.com/{}'.format(bucket_name, filename)
  try:
    with open(final_path, 'rb') as f:
      resp = requests.put(url, data=f, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
  except requests.exceptions.ConnectionError:
    my_log('ConnectionError')
  else:
    if resp.status_code != 200:
      my_log('error during put: {}, {}'.format(resp.status_code, resp.content))

def my_log(message):
  time_str = datetime.utcnow().replace(microsecond=0)
  sys.stderr.write("{} {} \n".format(time_str, message))

if __name__ == '__main__':
  my_log("intentional test error")
  screen_dir, thumb_dir, webcam_dir = init_dirs()

  # test with no internet
  original_put = requests.put

  def put_no_internet(*a, **kw):
    raise requests.exceptions.ConnectionError

  requests.put = put_no_internet

  temp_file = os_specific.take_screenshot()
  save_image(temp_file, os.path.join(screen_dir, 'test.png'))

  requests.put = original_put

  for _ in range(10):
    _0_mem_logger.log()
    temp_file = os_specific.take_screenshot()
    save_image(temp_file, os.path.join(screen_dir, 'test.png'))
    print 'saved image'
    save_image(temp_file, os.path.join(thumb_dir, 'test.png'), True)
    print 'saved thumbnail'

    time.sleep(5)
    os.remove(temp_file.name)
