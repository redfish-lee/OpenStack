#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *

def createKeystone():
  srcMysqlFile = "../lib/glance/create_keystone.sh"
  dstMysqlFile = "../tmp/create_keystone.sh"

  cmd = [
    Task("create  tmp dir        ", "mkdir -p ../tmp"),
    Task("create  mysql sh       ", "touch " + dstMysqlFile),
    Task("copy    mysql sh       ", "/bin/cp " + srcMysqlFile   + " " + dstMysqlFile),
    Task("chmod   mysql sh       ", "chmod +x " + dstMysqlFile),
  ]
  
  for task in cmd:
    task.exe()

  print "[INFO] replace mysql password"
  inplaceChange(dstMysqlFile, 'MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])

  print "[INFO] replace glance password"
  inplaceChange(dstMysqlFile, 'KEYSTONE_DBPASS', User.GLANCE[User.PASSWORD])

  cmd = [
    # mysql secure installation
    Task("install mysql secure   ", dstMysqlFile),
  ]
  for task in cmd:
    task.exe()

def installKeystone():
  cmd = [
    Task("install keystone       ", "yum install openstack-keystone httpd mod_wsgi python-openstackclient memcached python-memcached"),
    Task("create  mysql sh       ", "touch "),
    Task("copy    mysql sh       ", "/bin/cp " + srcMysqlFile   + " " + dstMysqlFile),
    Task("chmod   mysql sh       ", "chmod +x " + dstMysqlFile),
  ]
  
  for task in cmd:
    task.exe()


def main():
  createKeystone()
  installKeystone()


if __name__ == '__main__':
  main()