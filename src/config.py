#!/usr/bin/python
# -*- coding: UTF-8 -*-

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


