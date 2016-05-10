#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *


def createNeutron():
  Task("mkdir -p ../tmp")

  f = FileCopy("../lib/nova/create_nova.sh", "../tmp/create_nova.sh")
  f.replace('MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])
  f.replace('NEUTRON_DBPASS', User.NEUTRON[User.PASSWORD])
  f.exe()

def installNeutron():
  Source().admin()
  Task("openstack user create --password " + User.GLANCE[User.PASSWORD] + " neutron")
  Task("openstack role add --project service --user neutron admin")
  Task("openstack service create --name neutron \
          --description 'OpenStack Networking' network")
  Task("openstack endpoint create \
          --publicurl http://controller:9696 \
          --adminurl http://controller:9696 \
          --internalurl http://controller:9696 \
          --region RegionOne \
          network")

  install_list = [
    "openstack-neutron",
    "openstack-neutron-ml2",
    "python-neutronclient",
    "which",
  ]
  yumInstall(install_list)



  f = FileCopy("../lib/nova/nova.conf", "/etc/nova/nova.conf")
  f.replace('NOVA_DBPASS', User.NOVA[User.PASSWORD])
  f.replace('NOVA_PASS', User.NOVA[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])
  f.replace('CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])
  f.replace('MANAGEMENT_INTERFACE_IP_ADDRESS', Hosts.HOSTS_IP[Agent.CONTROLLER])

  Task("su -s /bin/sh -c 'nova-manage db sync' nova")

  Systemctl("openstack-nova-api.service", ["enable", "start"])
  Systemctl("openstack-nova-cert.service", ["enable", "start"])
  Systemctl("openstack-nova-consoleauth.service", ["enable", "start"])
  Systemctl("openstack-nova-scheduler.service", ["enable", "start"])
  Systemctl("openstack-nova-conductor.service", ["enable", "start"])
  Systemctl("openstack-nova-novncproxy.service", ["enable", "start"])

  install_list = [
    "openstack-nova-compute",
    "sysfsutils",
  ]
  yumInstall(install_list)

  Task("egrep -c '(vmx|svm)' /proc/cpuinfo")

  Systemctl("libvirtd.service", ["enable", "start"])
  Systemctl("openstack-nova-compute.service", ["enable", "start"])


def verify():
  Source().admin()
  Task("nova service-list")
  Task("nova endpoints")
  Task("nova image-list")

def main():
  """Install and configure controller node"""
  """Install and configure a compute node"""
  createNeutron()
  installNeutron()

  """Verify operation"""
  verify()


if __name__ == '__main__':
  main()