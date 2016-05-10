#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
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

  # use the 'original' only on stdout
  sys.stdout = original
  f.close()

def installBasic():


  install_list = [
    "http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-6.noarch.rpm",
    "http://rdo.fedorapeople.org/openstack-kilo/rdo-release-kilo.rpm",
    "openstack-selinux",
    "mariadb",
    "mariadb-server",
    "MySQL-python",
  ]

  yumInstall(install_list)
  Task("yum update -y")

def setupMariadbConfig():
  # edit /etc/my.cnf.d/mariadb_openstack.cnf
  f = FileCopy("../lib/mariadb/mariadb_openstack.cnf", "/etc/my.cnf.d/mariadb_openstack.cnf")
  f.replace('CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])

  # enable mariadb.service
  Systemctl("mariadb.service", ["enable", "start"])

  # mysql_secure_installation
  # lib/mariadb/mysql_secure.sh
  Task("mkdir -p ../tmp")
  yumInstall(['expect'])
  f = FileCopy("../lib/mariadb/mysql_secure.sh", "../tmp/mysql_secure.sh")
  f.replace('MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])
  f.exe()

  

def installRabbitmq():

  yumInstall(['rabbitmq-server'])
  Systemctl("rabbitmq-server.service", ["enable", "start"])

  # rabbitmqctl add_user openstack RABBIT_PASS
  Task("rabbitmqctl add_user " + User.RABBITMQ[User.ACCOUNT] + " " + User.RABBITMQ[User.PASSWORD])
  Task("rabbitmqctl set_permissions " + User.RABBITMQ[User.ACCOUNT] + " '.*' '.*' '.*'")
  
def closeFirewall():
  FileCopy("../lib/selinux/config", "/etc/selinux/config")

  print "success, reboot your computer now? (y/n)"
  ans = raw_input('> ')

  if ans in ['y', 'yes', 'Y', 'Yes', 'YES']:
    Task("reboot")



def main():
  """Set the hostname of the node to network"""
  addHosts()

  """OpenStack packages"""
  installBasic()

  """SQL database"""
  setupMariadbConfig()

  """Message queue"""
  installRabbitmq()

  closeFirewall()

if __name__ == '__main__':
  main()

