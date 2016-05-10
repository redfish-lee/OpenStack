#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

class User:
  ACCOUNT = "account"
  PASSWORD = "password"
  # all account is default, not used in setup
  ADMIN = {
    ACCOUNT: "admin",
    PASSWORD: "123456",
  }
  DEMO = {
    ACCOUNT: "demo",
    PASSWORD: "123456",
  }
  RABBITMQ = {
    ACCOUNT: "openstack",
    PASSWORD: "123456",
  }
  MYSQL = {
    ACCOUNT: "root",
    PASSWORD: "123456",
  }
  GLANCE = {
    ACCOUNT: "keystone",
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

class Source:
  def export(self, key, value):
    os.environ[key] = value

  def delexp(self, key):
    try:
      del os.environ[key]
    except:
      print "[WARN] unset " + key

  def admin(self):
    self.delexp('OS_SERVICE_TOKEN')
    self.export('OS_USERNAME'         , 'admin')
    self.export('OS_PASSWORD'         , User.ADMIN[User.PASSWORD])
    self.export('OS_AUTH_URL'         , 'http://controller:5000/v2.0')
    self.export('PS1'                 , '[\u@\h \W(keystone_admin)]\$ ')

    self.export('OS_TENANT_NAME'      , 'admin')
    self.export('OS_REGION_NAME'      , 'RegionOne')
    self.export('OS_IMAGE_API_VERSION', '2')

  def demo(self):
    self.delexp('OS_SERVICE_TOKEN')
    self.export('OS_USERNAME'         , 'demo')
    self.export('OS_PASSWORD'         , User.DEMO[User.PASSWORD])
    self.export('OS_AUTH_URL'         , 'http://controller:5000/v2.0')
    self.export('PS1'                 , '[\u@\h \W(keystone_demo)]\$ ')

    self.export('OS_TENANT_NAME'      , 'demo')
    self.export('OS_REGION_NAME'      , 'RegionOne')
    self.export('OS_IMAGE_API_VERSION', '2')










