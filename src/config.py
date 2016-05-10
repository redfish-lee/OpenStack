#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess

class User:
  ACCOUNT = "account"
  PASSWORD = "password"
  RABBITMQ = {
    ACCOUNT: "openstack",
    PASSWORD: "123456",
  }
  MYSQL = {
    ACCOUNT: "root",
    PASSWORD: "123456",
  }
  GLANCE = {
    ACCOUNT: "keystone"
    PASSWORD: "123456"
  }

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
