#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
