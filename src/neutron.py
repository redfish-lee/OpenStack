#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *


def createNeutron():
  Task("mkdir -p ../tmp")

  f = FileCopy("../lib/neutron/create_neutron.sh", "../tmp/create_neutron.sh")
  f.replace('MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])
  f.replace('NEUTRON_DBPASS', User.NEUTRON[User.PASSWORD])
  f.exe()

  Source().admin()
  Task("openstack user create --password " + User.NEUTRON[User.PASSWORD] + " neutron")
  Task("openstack role add --project service --user neutron admin")
  Task("openstack service create --name neutron \
          --description 'OpenStack Networking' network")
  Task("openstack endpoint create \
          --publicurl http://controller:9696 \
          --adminurl http://controller:9696 \
          --internalurl http://controller:9696 \
          --region RegionOne \
          network")

def installNeutron():
  f = FileCopy("../lib/neutron/sysctl.conf", "/etc/sysctl.conf")
  Task("sysctl -p")

  yumInstall("openstack-neutron")
  yumInstall("openstack-neutron-ml2")
  yumInstall("openstack-neutron-openvswitch")
  yumInstall("python-neutronclient")
  yumInstall("which")

  f = FileCopy("../lib/neutron/l3_agent.ini", "/etc/neutron/l3_agent.ini")
  f = FileCopy("../lib/neutron/dhcp_agent.ini", "/etc/neutron/dhcp_agent.ini")
  f = FileCopy("../lib/neutron/neutron.conf", "/etc/neutron/neutron.conf")
  f.replace('NEUTRON_DBPASS', User.NEUTRON[User.PASSWORD])
  f.replace('NEUTRON_PASS', User.NEUTRON[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])
  f.replace('NOVA_PASS', User.NOVA[User.PASSWORD])

  f = FileCopy("../lib/neutron/ml2_conf.ini", "/etc/neutron/plugins/ml2/ml2_conf.ini")
  f.replace('INSTANCE_TUNNELS_INTERFACE_IP_ADDRESS', Hosts.HOSTS_IP[Agent.NETWORK])

  f = FileCopy("../lib/neutron/nova.conf", "/etc/nova/nova.conf")
  f.replace('NOVA_DBPASS', User.NOVA[User.PASSWORD])
  f.replace('NOVA_PASS', User.NOVA[User.PASSWORD])
  f.replace('NEUTRON_PASS', User.NEUTRON[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])
  f.replace('CONTROLLER_IP', Hosts.HOSTS_IP[Agent.CONTROLLER])
  f.replace('MANAGEMENT_INTERFACE_IP_ADDRESS', Hosts.HOSTS_IP[Agent.CONTROLLER])
  f.replace('METADATA_SECRET', User.METADATA[User.PASSWORD])

  f = FileCopy("../lib/neutron/metadata_agent.ini", "/etc/neutron/metadata_agent.ini")
  f.replace('NEUTRON_PASS', User.NEUTRON[User.PASSWORD])
  f.replace('METADATA_SECRET', User.METADATA[User.PASSWORD])
  
  
  Task("ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini")
  Task("su -s /bin/sh -c 'neutron-db-manage --config-file /etc/neutron/neutron.conf \
          --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head' neutron")
  Task("cp /usr/lib/systemd/system/neutron-openvswitch-agent.service \
          /usr/lib/systemd/system/neutron-openvswitch-agent.service.orig")
  Task("sed -i 's,plugins/openvswitch/ovs_neutron_plugin.ini,plugin.ini,g' \
          /usr/lib/systemd/system/neutron-openvswitch-agent.service")

  Systemctl("openstack-nova-api.service", ["restart"])
  Systemctl("openstack-nova-scheduler.service", ["restart"])
  Systemctl("openstack-nova-conductor.service", ["restart"])
  
  Systemctl("neutron-server.service", ["enable", "start"])
  Systemctl("openvswitch.service", ["enable", "start"])
  Task("ovs-vsctl add-br br-ex")
  Task("ovs-vsctl add-port br-ex " + Network.INTERFACE_NAME)
   
  Systemctl("neutron-l3-agent.service", ["enable", "start"])
  Systemctl("neutron-dhcp-agent.service", ["enable", "start"]) 
  Systemctl("neutron-metadata-agent.service", ["enable", "start"])
  Systemctl("neutron-ovs-cleanup.service", ["enable"])

  Systemctl("openstack-nova-compute.service", ["restart"])
  Systemctl("neutron-openvswitch-agent.service", ["enable", "start"])

def verify():
  Source().admin()
  # Install and configure controller node
  Task("neutron ext-list")

  # Install and configure network node
  # Install and configure compute node
  Task("neutron agent-list")

def main():
  createNeutron()
  installNeutron()
  
  verify()


if __name__ == '__main__':
  main()