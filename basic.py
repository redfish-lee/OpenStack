#!/usr/bin/python
# -*- coding: UTF-8 -*-

import shlex, subprocess, os, sys

class Agent:
  CONTROLLER = "controller"
  NETWORK = "network"
  COMPUTE = "compute"


class Hosts:
  HOSTS_DIR = "/etc/hosts"
  HOSTS_IP = {
    Agent.CONTROLLER: "127.0.0.1",
    Agent.NETWORK: "127.0.0.1",
    Agent.COMPUTE: "127.0.0.1",
  }

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

def main():

  f = open(Hosts.HOSTS_DIR, 'a')
  original = sys.stdout
  sys.stdout = Tee(sys.stdout, f)
  # This will go to stdout and the file out.txt
  #print "test"  

  for key, value in Hosts.HOSTS_IP.iteritems():
    content = value + "   " + key
    print content

  #use the original
  sys.stdout = original
  print "[INFO] add ip on hosts"  # Only on stdout
  f.close()

if __name__ == '__main__':
  main()

