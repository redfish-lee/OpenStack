#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Task:
  def __init__(self, command, info=None):
    self.info = command if info is None else info
    self.command  = command
    self.exe()
  def info(self):
    return self.info
  def command(self):
    return self.command
  def exe(self):
    print "[INFO] " + self.info
    subprocess.call(self.command.split())

class FileCopy:
  def __init__(self, src, dst):
    self.src = src
    self.dst = dst
    self.copy()
  
  def src(self):
    return self.src
  
  def dst(self):
    return self.dst
  
  def chmod(self, per, dst = None):
    dst = self.dst if dst is None else dst
    Task("chmod "   + per + " " + dst)
  
  def copy(self, src = None, dst = None):
    dst = self.dst if dst is None else dst
    src = self.src if src is None else src
    Task("touch "   + dst)
    Task("/bin/cp " + src + " " + dst)
  
  def replace(self, old_string, new_string, dst = None):
    dst = self.dst if dst is None else dst
    print "[INFO] replace", dst
    inplaceChange(dst, old_string, new_string)

  def exe(dst = None):
    dst = self.dst if dst is None else dst
    self.chmod("+x")
    Task(dst)

class Systemctl():
  def __init__(self, service, stat):
    self.status = status
    self.service = service
    self.exe()

  def exe(self):
    for stat in self.status:
      Task("systemctl " +  stat + " " + self.service)

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

def yumInstall(install_list):
  for item in install_list:
    Task("yum install " + item + " -y")

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