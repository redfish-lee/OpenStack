#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Task:
  def __init__(self, info, command):
    self.info = info
    self.command  = command
  def info(self):
    return self.info
  def command(self):
    return self.command
  def exe(self):
    print "[INFO] " + self.info
    subprocess.call(self.command.split())

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

def inplaceChange(filename, old_string, new_string):
  # Safely read the input filename using 'with'
  with open(filename) as f:
    s = f.read()
    if old_string not in s:
      print '"{old_string}" not found in {filename}.'.format(**locals())
      return

  # Safely write the changed content, if found in the file
  with open(filename, 'w') as f:
    print 'Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals())
    s = s.replace(old_string, new_string)
    f.write(s)