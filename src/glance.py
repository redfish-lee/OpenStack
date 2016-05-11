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

  Source().admin()
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

def installGlance():
  install_list = [
    "openstack-glance",
    "python-glance",
    "python-glanceclient",
  ]
  yumInstall(install_list)

  f = FileCopy("../lib/glance/glance-api.conf", "/etc/glance/glance-api.conf")
  f.replace('GLANCE_DBPASS', User.GLANCE[User.PASSWORD])
  f.replace('GLANCE_PASS', User.GLANCE[User.PASSWORD])

  f = FileCopy("../lib/glance/glance-registry.conf", "/etc/glance/glance-registry.conf")
  f.replace('GLANCE_DBPASS', User.GLANCE[User.PASSWORD])
  f.replace('GLANCE_PASS', User.GLANCE[User.PASSWORD])  

  Task("su -s /bin/sh -c 'glance-manage db_sync' glance")
  Systemctl("openstack-glance-api.service", ["enable", "start"])
  Systemctl("openstack-glance-registry.service", ["enable", "start"])

def fixBugImages():
  # after update 20160501
  f = FileCopy("../lib/bugs/images.py", "/usr/lib/python2.7/site-packages/glanceclient/v1/images.py")
  Task("rm -f /usr/lib/python2.7/site-packages/glanceclient/v1/images.pyc")
  Task("rm -f /usr/lib/python2.7/site-packages/glanceclient/v1/images.pyo")

def verify():
  Source().admin()
  Task("mkdir /tmp/images")
  Task("wget -P /tmp/images http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img")
  Task("glance image-create --name 'cirros-0.3.4-x86_64' --file /tmp/images/cirros-0.3.4-x86_64-disk.img \
          --disk-format qcow2 --container-format bare --visibility public --progress")
  Task("glance image-list")
  Task("rm -r /tmp/images")

def main():
  createGlance()
  installGlance()
  fixBugImages()
  verify()


if __name__ == '__main__':
  main()