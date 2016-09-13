import resource

class MemoryLogger:
  def __init__(self):
    self.prev_mem, self.curr_mem = None, None
    self.num_increases, self.total_checks = 0, 0

  def log(self, flag):
    colors = pink, blue, green, yellow, red = (
        '\033[95m', '\033[94m', '\033[92m', '\033[93m', '\033[91m')
    end = '\033[0m'
    self.prev_mem = self.curr_mem
    self.curr_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print 'curr_mem {}:'.format(flag),
    self.total_checks += 1
    if self.prev_mem and self.curr_mem > self.prev_mem:
      self.num_increases += 1
      print pink, self.curr_mem, end, self.num_increases, self.total_checks
    else:
      print self.curr_mem

mem_log = MemoryLogger()
def log(flag=''):
  mem_log.log(flag)

if __name__ == '__main__':
  mem_log = MemoryLogger()
  mem_log.log('test')
  import time
  mem_log.log('test2')
