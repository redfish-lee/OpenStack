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
  
    print "[INFO] installing epel"
    cmd = "yum install http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-6.noarch.rpm -y"
    subprocess.call(cmd.split())

    print "[INFO] update centos"
    cmd = "yum update -y"
    subprocess.call(cmd.split())

    print "[INFO] install openstack selinux"
    cmd = "yum install openstack-selinux -y"
    subprocess.call(cmd.split())

    print "[INFO] installing mariadb"
    cmd = "yum update -y"
    subprocess.call(cmd.split())

def setup_mariadb_config():
  
  print "[INFO] copy mariadb config file"
  srcFile = "./lib/mariadb/mariadb_openstack.cnf "
  dstFile = "/etc/my.cnf.d/mariadb_openstack.cnf "
  cmd = "cp " + srcFile + dstFile + "-i"
  subprocess.call(cmd.split())

  print "[INFO] update controller ip"
  func.inplace_change(dstFile, 'CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])

  print "[INFO] enable mariadb service"
  cmd = "systemctl enable mariadb.service"
  subprocess.call(cmd.split())

  print "[INFO] start mariadb service"
  cmd = "systemctl start mariadb.service"
  subprocess.call(cmd.split())

  print "[INFO] mysql secure installation"
  cmd = "mysql_secure_installation"
  subprocess.call(cmd.split())
  

def install_rabbitmq():
  
  print "[INFO] installing rabbitmq server"
  cmd = "yum install rabbitmq-server -y"
  subprocess.call(cmd.split())

  print "[INFO] enable rabbitmq server service"
  cmd = "systemctl enable rabbitmq-server.service"
  subprocess.call(cmd.split())

  print "[INFO] start rabbitmq server service"
  cmd = "systemctl start rabbitmq-server.service"
  subprocess.call(cmd.split())

  print "[INFO] start rabbitmq server service"
  # rabbitmqctl add_user openstack RABBIT_PASS
  cmd = "rabbitmqctl add_user " + User.RABBITMQ[ACCOUNT] + " " + User.RABBITMQ[PASSWORD]
  subprocess.call(cmd.split())
  
  print "[INFO] start rabbitmq server service"
  cmd = "rabbitmqctl set_permissions " + User.RABBITMQ[ACCOUNT] + " '.*' '.*' '.*'"
  subprocess.call(cmd.split())
  


def main():
  add_hosts()
  install_basic()
  setup_mariadb_config()
  install_rabbitmq()

if __name__ == '__main__':
  main()

