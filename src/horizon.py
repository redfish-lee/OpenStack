#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *

def installHorizon():
  yumInstall("openstack-dashboard")
  yumInstall("httpd")
  yumInstall("mod_wsgi")
  yumInstall("memcached")
  yumInstall("python-memcached")

  FileCopy("../lib/horizon/local_settings", "/etc/openstack-dashboard/local_settings")

  Task("setsebool -P httpd_can_network_connect on")
  Task("chown -R apache:apache /usr/share/openstack-dashboard/static")
  Systemctl("httpd.service", ["enable", "start"])
  Systemctl("memcached.service", ["enable", "start"])

def main():
  installHorizon()

  # reboot for configure fixed bugs
  rebootComputer()

  # verify
  # open the page "http://controller/dashboard/" on browser

if __name__ == '__main__':
  main()