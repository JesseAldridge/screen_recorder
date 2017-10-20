import win32api, ImageGrab

def get_screen_size():
  return [win32api.GetSystemMetrics(i) for i in range(2)]

def take_screenshot():
  return ImageGrab.grab()

def take_webcam_image():
  # todo
  pass

if __name__ == '__main__':
  print get_screen_size()
