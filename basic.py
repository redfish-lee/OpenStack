#!/usr/bin/python
# -*- coding: UTF-8 -*-

import shlex, subprocess, os, sys
from config import *
from func import *

def add_hosts():
  
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
    # sys.stdout = original
    f.close()

def install_basic():
  
  cmd = {}
  cmd["install epel           "] = "yum install http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-6.noarch.rpm -y"
  cmd["update  centos         "] = "yum update -y"
  cmd["install selinux        "] = "yum install openstack-selinux -y"
  cmd["install mariadb        "] = "yum install mariadb mariadb-server MySQL-python -y"

  for key, value in cmd.iteritems():
    print "[INFO] " + key
    subprocess.call(value.split())

def setup_mariadb_config():

  srcMariadbFile = "./lib/mariadb/mariadb_openstack.cnf "
  dstMariadbFile = "/etc/my.cnf.d/mariadb_openstack.cnf "
  srcMysqlFile = "./lib/mariadb/mysql_secure.sh "
  dstMysqlFile = "./tmp/mysql_secure.sh"

  cmd = {}
  cmd["copy    mariadb config "] = "/bin/cp " + srcMariadbFile + dstMariadbFile
  cmd["copy    mysql secure sh"] = "/bin/cp " + srcMysqlFile   + dstMysqlFile
  for key, value in cmd.iteritems():
    if value is 
    print "[INFO] " + key
    subprocess.call(value.split())

  print "[INFO] update  controller ip"
  func.inplace_change(dstMariadbFile, 'CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])

  print "[INFO] replace mysql password"
  func.inplace_change(dstMariadbFile, 'MYSQL_PASSWORD', User.MYSQL[PASSWORD])

  cmd = {}
  cmd["enable  mariadb service"] = "systemctl enable mariadb.service"
  cmd["start   mariadb service"] = "systemctl start mariadb.service"
  cmd["install mysql secure   "] = dstMysqlFile
  for key, value in cmd.iteritems():
    print "[INFO] " + key
    subprocess.call(value.split())
  

def install_rabbitmq():

  cmd = {}
  cmd["install rabbitmq server"] = "yum install rabbitmq-server -y"
  cmd["enable  rabbitmq server"] = "systemctl enable rabbitmq-server.service"
  cmd["start   rabbitmq server"] = "systemctl start rabbitmq-server.service"
  # rabbitmqctl add_user openstack RABBIT_PASS
  cmd[""] = "rabbitmqctl add_user " + User.RABBITMQ[ACCOUNT] + " " + User.RABBITMQ[PASSWORD]
  cmd[""] = "rabbitmqctl set_permissions " + User.RABBITMQ[ACCOUNT] + " '.*' '.*' '.*'"

  for key, value in cmd.iteritems():
    print "[INFO] " + key
    subprocess.call(value.split())
  
def main():
  add_hosts()
  install_basic()
  setup_mariadb_config()
  install_rabbitmq()

if __name__ == '__main__':
  main()

