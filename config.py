import os, json

config_path = os.path.expanduser('~/.screen_recorder_config')
config_dict = {}
if os.path.exists(config_path):
  with open(config_path) as f:
    json_text = f.read()
  config_dict = json.loads(json_text)

if __name__ == '__main__':
  print config_dict
