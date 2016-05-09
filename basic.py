#!/usr/bin/python
# -*- coding: UTF-8 -*-

import shlex, subprocess, os, sys
from config import *
from func import *

def addHosts():
  
    print "[INFO] add ip on hosts"
    f = open(Hosts.HOSTS_DIR, 'a')
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, f)
    # This will go to stdout and the file out.txt
    #print "test"  

    for key, value in Hosts.HOSTS_IP.iteritems():
      if key not in open(Hosts.HOSTS_DIR).read():
        content = value + "   " + key
        print content

    # use the original
    # Only on stdout
    sys.stdout = original
    f.close()

def installBasic():

  cmd = [
    Task("install epel           ", "yum install http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-6.noarch.rpm -y"),
    Task("update  centos         ", "yum update -y"),
    Task("install selinux        ", "yum install openstack-selinux -y"),
    Task("install mariadb        ", "yum install mariadb mariadb-server MySQL-python -y"),
  ]

  for task in cmd:
    task.exe()

def setupMariadbConfig():

  srcMariadbFile = "./lib/mariadb/mariadb_openstack.cnf"
  dstMariadbFile = "/etc/my.cnf.d/mariadb_openstack.cnf"
  srcMysqlFile = "./lib/mariadb/mysql_secure.sh"
  dstMysqlFile = "./tmp/mysql_secure.sh"

  cmd = [
    Task("create  tmp dir        ", "mkdir -p ./tmp"),
    Task("create  mysql secure sh", "touch " + dstMysqlFile),
    Task("copy    mariadb config ", "/bin/cp " + srcMariadbFile + " " + dstMariadbFile),
    Task("copy    mysql secure sh", "/bin/cp " + srcMysqlFile   + " " + dstMysqlFile),
    Task("chmod   mysql secure sh", "chmod +x " + dstMysqlFile),
  ]
  for task in cmd:
    task.exe()

  print "[INFO] replace controller ip "
  inplaceChange(dstMariadbFile, 'CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])

  print "[INFO] replace mysql password"
  inplaceChange(dstMysqlFile, 'MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])

  cmd = [
    Task("enable  mariadb service", "systemctl enable mariadb.service"),
    Task("start   mariadb service", "systemctl start mariadb.service"),

    Task("install expect         ", "yum install expect -y"),
    Task("install mysql secure   ", dstMysqlFile),              # need expect
  ]
  for task in cmd:
    task.exe()
  

def installRabbitmq():

  cmd = [
    Task("install rabbitmq server", "yum install rabbitmq-server -y"),
    Task("enable  rabbitmq server", "systemctl enable rabbitmq-server.service"),
    Task("start   rabbitmq server", "systemctl start rabbitmq-server.service"),
    # rabbitmqctl add_user openstack RABBIT_PASS
    Task("rabbit  add user       ", "rabbitmqctl add_user " + User.RABBITMQ[User.ACCOUNT] + " " + User.RABBITMQ[User.PASSWORD]),
    Task("rabbit  set permissions", "rabbitmqctl set_permissions " + User.RABBITMQ[User.ACCOUNT] + " '.*' '.*' '.*'"),
  ]

  for task in cmd:
    task.exe()
  
def main():
  addHosts()
  installBasic()
  setupMariadbConfig()
  installRabbitmq()

if __name__ == '__main__':
  main()

