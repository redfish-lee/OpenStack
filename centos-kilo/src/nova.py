#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *


def createNova():
  Task("mkdir -p ../tmp")

  f = FileCopy("../lib/nova/create_nova.sh", "../tmp/create_nova.sh")
  f.replace('MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])
  f.replace('NOVA_DBPASS', User.NOVA[User.PASSWORD])
  f.exe()
  Source().admin()
  Task("openstack user create --password " + User.NOVA[User.PASSWORD] + " nova")
  Task("openstack role add --project service --user nova admin")
  Task("openstack service create --name nova \
          --description 'OpenStack Compute' compute")
  Task("openstack endpoint create \
          --publicurl http://controller:8774/v2/%\(tenant_id\)s \
          --internalurl http://controller:8774/v2/%\(tenant_id\)s \
          --adminurl http://controller:8774/v2/%\(tenant_id\)s \
          --region RegionOne \
          compute")

def installNova():
  yumInstall("openstack-nova-api")
  yumInstall("openstack-nova-cert")
  yumInstall("openstack-nova-conductor")
  yumInstall("openstack-nova-console")
  yumInstall("openstack-nova-novncproxy")
  yumInstall("openstack-nova-scheduler")
  yumInstall("python-novaclient")
  yumInstall("openstack-nova-compute")
  yumInstall("sysfsutils")

  f = FileCopy("../lib/nova/nova.conf", "/etc/nova/nova.conf")
  f.replace('NOVA_DBPASS', User.NOVA[User.PASSWORD])
  f.replace('NOVA_PASS', User.NOVA[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])
  f.replace('CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])
  f.replace('MANAGEMENT_INTERFACE_IP_ADDRESS', Hosts.HOSTS_IP[Agent.CONTROLLER])

  Task("su -s /bin/sh -c 'nova-manage db sync' nova")
  Task("egrep -c '(vmx|svm)' /proc/cpuinfo")

  Systemctl("openstack-nova-api.service", ["enable", "start"])
  Systemctl("openstack-nova-cert.service", ["enable", "start"])
  Systemctl("openstack-nova-consoleauth.service", ["enable", "start"])
  Systemctl("openstack-nova-scheduler.service", ["enable", "start"])
  Systemctl("openstack-nova-conductor.service", ["enable", "start"])
  Systemctl("openstack-nova-novncproxy.service", ["enable", "start"])
  Systemctl("openstack-nova-compute.service", ["enable", "start"])
  Systemctl("libvirtd.service", ["enable", "start"])

def verify():
  Source().admin()
  Task("nova service-list")
  Task("nova endpoints")
  Task("nova image-list")

def main():
  createNova()
  installNova()
  
  verify()


if __name__ == '__main__':
  main()