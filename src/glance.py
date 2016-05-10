#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *


def createGlance():
  Task("mkdir -p ../tmp")

  f = FileCopy("../lib/glance/create_glance.sh", "../tmp/create_glance.sh")
  f.replace('MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])
  f.replace('GLANCE_DBPASS', User.GLANCE[User.PASSWORD])
  f.exe()

def installGlance():
  Task("openstack user create --password " + User.GLANCE[User.PASSWORD] + " glance")
  Task("openstack role add --project service --user glance admin")
  Task("openstack service create --name glance \
          --description 'OpenStack Image service' image")
  Task("openstack endpoint create \
          --publicurl http://controller:9292 \
          --internalurl http://controller:9292 \
          --adminurl http://controller:9292 \
          --region RegionOne \
          image")

  install_list = [
    "openstack-glance",
    "python-glance",
    "python-glanceclient",
  ]

  yumInstall(install_list)

  Task("")
  Task("")
  Task("")
  
  Task("su -s /bin/sh -c 'glance-manage db_sync' glance")
  Systemctl("openstack-glance-api.service", ["enable", "start"])
  Systemctl("openstack-glance-registry.service", ["enable", "start"])

def verify():
  Source.admin()
  Task("mkdir /tmp/images")
  Task("wget -P /tmp/images http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img")
  Task("glance image-create --name 'cirros-0.3.4-x86_64' --file /tmp/images/cirros-0.3.4-x86_64-disk.img \
          --disk-format qcow2 --container-format bare --visibility public --progress")
  Task("glance image-list")
  Task("rm -r /tmp/images")



def main():
  """Install and configure"""
  createGlance()

  """Install and configure"""
  installGlance()

  """Verify operation"""
  verify()


if __name__ == '__main__':
  main()