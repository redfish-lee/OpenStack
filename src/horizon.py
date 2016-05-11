#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *

def installHorizon():
  install_list = [
    "openstack-dashboard",
    "httpd",
    "mod_wsgi",
    "memcached",
    "python-memcached",
  ]
  yumInstall(install_list)

  FileCopy("../lib/horizon/local_settings", "/etc/openstack-dashboard/local_settings")

  Task("setsebool -P httpd_can_network_connect on")
  Task("chown -R apache:apache /usr/share/openstack-dashboard/static")
  Systemctl("httpd.service", ["enable", "start"])
  Systemctl("memcached.service", ["enable", "start"])

def main():
  installHorizon()

if __name__ == '__main__':
  main()