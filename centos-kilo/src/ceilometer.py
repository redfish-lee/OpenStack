#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands
from config import *
from func import *


def installMongodb():
  yumInstall("mongodb-server")
  yumInstall("mongodb")

  f = FileCopy("../lib/ceilometer/mongod.conf", "/etc/mongod.conf")
  f.replace('CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])

  Systemctl("mongod.service", ["enable", "start"])

  Task("mongo --host controller --eval \'    \
          db = db.getSiblingDB(\"ceilometer\");   \
          db.createUser({user: \"ceilometer\",   \
          pwd: \"" + User.CEILOMETER[User.PASSWORD] + "\",   \
          roles: [ \"readWrite\", \"dbAdmin\" ]})\'")

  Source().admin()
  Task("openstack user create --password " + User.CEILOMETER[User.PASSWORD] + " ceilometer")
  Task("openstack role add --project service --user ceilometer admin")
  Task("openstack service create --name ceilometer \
          --description 'Telemetry' metering")
  Task("openstack endpoint create \
          --publicurl http://controller:8777 \
          --internalurl http://controller:8777 \
          --adminurl http://controller:8777 \
          --region RegionOne \
          metering")

def installTelemetry():
  yumInstall("openstack-ceilometer-api")
  yumInstall("openstack-ceilometer-collector")
  yumInstall("openstack-ceilometer-notification")
  yumInstall("openstack-ceilometer-central")
  yumInstall("openstack-ceilometer-alarm")
  yumInstall("python-ceilometerclient")

  f = FileCopy("../lib/ceilometer/ceilometer.conf", "/etc/ceilometer/ceilometer.conf")
  f.replace("CEILOMETER_DBPASS", User.CEILOMETER[User.PASSWORD])
  f.replace("CEILOMETER_PASS", User.CEILOMETER[User.PASSWORD])
  f.replace("TELEMETRY_SECRET", User.CEILOMETER[User.PASSWORD])
  f.replace("RABBIT_PASS", User.RABBITMQ[User.PASSWORD])

  Systemctl("mongod.service", ["enable", "start"])

  Systemctl("openstack-ceilometer-api.service", ["enable", "start"])
  Systemctl("openstack-ceilometer-notification.service", ["enable", "start"])
  Systemctl("openstack-ceilometer-central.service", ["enable", "start"])
  Systemctl("openstack-ceilometer-collector.service", ["enable", "start"])
  Systemctl("openstack-ceilometer-alarm-evaluator.service", ["enable", "start"])
  Systemctl("openstack-ceilometer-alarm-notifier.service", ["enable", "start"])


def configureCompute():
  yumInstall("openstack-ceilometer-compute")
  yumInstall("python-ceilometerclient")
  yumInstall("python-pecan")

  f = FileCopy("../lib/ceilometer/ceilometer.conf", "/etc/ceilometer/ceilometer.conf")
  f.replace("CEILOMETER_DBPASS", User.CEILOMETER[User.PASSWORD])
  f.replace("CEILOMETER_PASS", User.CEILOMETER[User.PASSWORD])
  f.replace("TELEMETRY_SECRET", User.CEILOMETER[User.PASSWORD])
  f.replace("RABBIT_PASS", User.RABBITMQ[User.PASSWORD])

  f = FileCopy("../lib/ceilometer/nova.conf", "/etc/nova/nova.conf")
  f.replace('NOVA_DBPASS', User.NOVA[User.PASSWORD])
  f.replace('NOVA_PASS', User.NOVA[User.PASSWORD])
  f.replace('NEUTRON_PASS', User.NEUTRON[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])
  f.replace('CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])
  f.replace('MANAGEMENT_INTERFACE_IP_ADDRESS', Hosts.HOSTS_IP[Agent.CONTROLLER])
  f.replace('METADATA_SECRET', User.METADATA[User.PASSWORD])

  Systemctl("openstack-ceilometer-compute.service", ["enable", "start"])
  Systemctl("openstack-nova-compute.service", ["restart"])

def configureImage():
  f = FileCopy("../lib/ceilometer/glance-api.conf", "/etc/glance/glance-api.conf")
  f.replace('GLANCE_DBPASS', User.GLANCE[User.PASSWORD])
  f.replace('GLANCE_PASS', User.GLANCE[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])
  
  f = FileCopy("../lib/ceilometer/glance-registry.conf", "/etc/glance/glance-registry.conf")
  f.replace('GLANCE_DBPASS', User.GLANCE[User.PASSWORD])
  f.replace('GLANCE_PASS', User.GLANCE[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])

  Systemctl("openstack-glance-api.service", ["restart"])
  Systemctl("openstack-glance-registry.service", ["restart"])


def configureBlock():
  """no install block"""

def verify():
  Source().admin()
  Task("ceilometer meter-list")

  image_id = commands.getoutput("(glance image-list | grep 'cirros-0.3.4-x86_64' | awk '{ print $2 }')")
  Task("glance image-download " + image_id + " > /tmp/cirros.img")

  Task("ceilometer meter-list")
  Task("ceilometer statistics -m image.download -p 60")
  Task("rm /tmp/cirros.img")

def main():
  installMongodb()
  installTelemetry()

  configureCompute()
  configureImage()
  configureBlock()
  
  verify()


if __name__ == '__main__':
  main()