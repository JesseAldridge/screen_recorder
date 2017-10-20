import subprocess, os, time, re, tempfile
from datetime import datetime

class g:
  cached_size = None

def get_screen_size(write_to_disk=True):
  if not g.cached_size:
    g.cached_size = [0, 0]
    proc = subprocess.Popen(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE)
    result = proc.communicate()[0]
    match = re.search('Resolution.*', result)
    dims = match.group().split(':')[-1].split('x')
    if match:
      g.cached_size = [int(re.sub('[^0-9]', '', s)) for s in dims]
    # (I think system_profiler can fail around shutdown or startup, so fallback to file.)
    elif write_to_disk:
      with open(os.path.expanduser('~/.screen_size')) as f:
        g.cached_size = f.read().split()
    if write_to_disk:
      with open(os.path.expanduser('~/.screen_size'), 'w') as f:
        f.write(' '.join([str(x) for x in g.cached_size]))
  return g.cached_size

def take_screenshot():
  ' Return an Image of the screen. '

  tf = tempfile.NamedTemporaryFile(delete=False)
  cmd_line = 'screencapture -t png -x {}'.format(tf.name)
  subprocess.Popen(cmd_line.split()).communicate()
  return tf

def take_webcam_image(dir_path):
  ' Take a snapshot and save to passed dir. '

  filename = datetime.now().strftime('%Y-%m-%d_%H.%M.%S') + '.png'
  out_path = os.path.join(dir_path, filename)
  print 'out_path:', out_path
  subprocess.Popen(['/usr/local/bin/imagesnap', out_path]).communicate()

if __name__ == '__main__':
  for i in range(10):
    print get_screen_size()
  for i in range(2):
    print take_screenshot()
    take_webcam_image(os.getcwd())
    time.sleep(1)
