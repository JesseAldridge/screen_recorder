#!/usr/bin/python

import glob, os, shutil, time, resource, sys, json
from datetime import datetime, timedelta

import psutil, pytz

import _1_save_image, _0_mem_logger
from _1_save_image import os_specific
import config

SECS_PER_SHOT = config.config_dict.get('secs_per_shot', 5)
NUM_DAYS_TO_SAVE = 3 # dropped from 6 to 3 because taking too much hard drive space
debug_mode = True

def start_capturing(total_shots=None):
  ' Save a png of the screen every several seconds. Pause on low memory. '

  initial_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  max_mem = initial_memory * 2.5
  log('will stop if memory exceeds:', max_mem)

  def loop():
    num_shots = 0
    while True:
      curr_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
      log('curr_mem:', curr_mem)
      if curr_mem > max_mem:
        log('using too much memory according to resource.getrusage')

      remove_old_screenshots()
      num_shots += 1
      if total_shots is not None and num_shots > total_shots:
        break
      mem_percent = psutil.virtual_memory().percent
      if mem_percent < 90:
        capture_frame()
      else:
        log('skipping screenshot due to memory usage')
      time.sleep(SECS_PER_SHOT)
  try:
    loop()
  except Exception as e:
    _1_save_image.my_log(unicode(e))
    if debug_mode:
      _1_save_image.my_log('quitting because debug_mode is on')
      raise

def remove_old_screenshots():
  keep_after_date = datetime.now() - timedelta(hours=24 * NUM_DAYS_TO_SAVE)
  log('keep_after_date:', keep_after_date)
  dir_path = _1_save_image.screens_path
  for paths in (
    glob.glob(os.path.join(dir_path, "*.png")),
    glob.glob(os.path.join(dir_path, "thumbnails", "*.png")),
    glob.glob(os.path.join(dir_path, "webcam", "*.jpg")),
  ):
    for path in sorted(paths):
      try:
        file_dt = datetime.strptime(os.path.basename(path).split(".png")[0], '%Y-%m-%d_%H.%M.%S')
      except ValueError:
        log('value error, path: {}'.format(path))
        continue
      if file_dt > keep_after_date:
        break
      if path.endswith(".png") or path.endswith(".jpg"):
        log('deleting:', path)
        os.remove(path)


def capture_frame():
  ' Take a screenshot.  Save the image and thumbnail.  Log errors. '

  screen_dir, thumb_dir, webcam_dir = _1_save_image.init_dirs()

  try:
    temp_file = os_specific.take_screenshot()
    # os_specific.take_webcam_image(webcam_dir)
  except IOError as e:
    _1_save_image.my_log("I/O error({0}): {1}".format(e.errno, e.strerror))
  else:
    timestamp = '_'.join(str(datetime.utcnow()).split()).replace(':', '.').rsplit('.', 1)[0]
    filename = timestamp + '.png'

    log('filename:', filename)
    _1_save_image.save_image(temp_file, os.path.join(screen_dir, filename))
    _1_save_image.save_image(temp_file, os.path.join(thumb_dir, filename), is_thumb=True)
  finally:
    os.remove(temp_file.name)

def log(*args):
  iso_timestamp = pytz.timezone("UTC").localize(datetime.utcnow()).isoformat()
  print '{} {}'.format(iso_timestamp, ' '.join(str(x) for x in args))

if __name__ == '__main__':
  start_capturing()

  # import cProfile, pstats
  # def read_results():
  #   p = pstats.Stats('profile_results.txt')
  #   p.strip_dirs().sort_stats('cumulative').print_stats(10)
  # cProfile.run("grab_pngs(3)", 'profile_results.txt')
  # read_results()
