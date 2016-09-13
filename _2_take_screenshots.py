#!/usr/bin/python

import glob, os, shutil, time, resource, sys
from datetime import datetime, timedelta

import psutil

import _1_save_image, _0_mem_logger
from _1_save_image import os_specific

secs_per_shot = 5
debug_mode = True

def grab_pngs(total_shots=None):
  ' Save a png of the screen every several seconds. Pause on low memory. '

  initial_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  max_mem = initial_memory * 2.5
  print 'will stop if memory exceeds:', max_mem

  def loop():
    num_shots = 0
    while True:
      curr_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
      if curr_mem > max_mem:
        print 'using too much memory'

      remove_old_screenshots()
      num_shots += 1
      if total_shots is not None and num_shots > total_shots:
        break
      mem_percent = psutil.virtual_memory().percent
      if mem_percent < 90:
        save_tagged_screenshot()
      time.sleep(secs_per_shot)
  try:
    loop()
  except Exception as e:
    _1_save_image.my_log(unicode(e))
    if debug_mode:
      raise

def remove_old_screenshots():
  ' Remove screenshots over 24 hours old. '

  yesterday = datetime.now() - timedelta(hours=24)
  print 'yesterday:', yesterday
  dir_path = _1_save_image.screens_path
  for paths in (
    glob.glob(os.path.join(dir_path, "*.png")),
    glob.glob(os.path.join(dir_path, "thumbnails", "*.png"))):
    for path in paths:
      try:
        file_dt = datetime.strptime(os.path.basename(path).split(".png")[0], '%Y-%m-%d_%H.%M.%S')
      except ValueError:
        continue
      if file_dt > yesterday:
        break
      assert path.endswith(".png")
      os.remove(path)

def save_tagged_screenshot():
  ' Take a screenshot.  Save the image and thumbnail.  Log errors. '

  screen_dir, thumb_dir = _1_save_image.init_dirs()

  try:
    temp_file = os_specific.take_screenshot()
  except IOError as e:
    _1_save_image.my_log("I/O error({0}): {1}".format(e.errno, e.strerror))
  else:
    timestamp = '_'.join(str(
        datetime.now()).split()).replace(':', '.').rsplit('.', 1)[0]
    filename = timestamp + '.png'

    print 'filename:', filename
    _1_save_image.save_image(temp_file, os.path.join(screen_dir, filename))
    _1_save_image.save_image(
      temp_file, os.path.join(thumb_dir, filename), is_thumb=True)
  finally:
    os.remove(temp_file.name)

if __name__ == '__main__':
  grab_pngs()

  # import cProfile, pstats
  # def read_results():
  #   p = pstats.Stats('profile_results.txt')
  #   p.strip_dirs().sort_stats('cumulative').print_stats(10)
  # cProfile.run("grab_pngs(3)", 'profile_results.txt')
  # read_results()
