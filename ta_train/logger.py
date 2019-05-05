import sys


def info(msg, *args):
  if len(args) > 0:
    sys.stdout.write(msg % args)
  else:
    sys.stdout.write(msg)
  sys.stdout.write('\n')
  
def warn(msg, *args):
  if len(args) > 0:
    sys.stderr.write(msg % args)
  else:
    sys.stderr.write(msg)
  sys.stderr.write('\n')