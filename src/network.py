#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *


def createExternalNetwork():
  Source().admin()
  Task("neutron net-create ext-net --router:external \
          --provider:physical_network external --provider:network_type flat")
  Task("neutron subnet-create ext-net " + Network.EXTERNAL_NETWORK_CIDR + " --name ext-subnet \
          --allocation-pool start=" + Network.FLOATING_IP_START + ",end=" + Network.FLOATING_IP_END + " \
          --disable-dhcp --gateway " + Network.EXTERNAL_NETWORK_GATEWAY)

def createTenantNetwork():
  Source().admin()
  Task("neutron net-create demo-net")
  Task("neutron subnet-create demo-net " + Network.TENANT_NETWORK_CIDR + " \
          --name demo-subnet --dns-nameserver " + Network.DNS_RESOLVER + " \
          --gateway " + Network.TENANT_NETWORK_GATEWAY)

  # Router
  Task("neutron router-create demo-router")
  Task("neutron router-interface-add demo-router demo-subnet")
  Task("neutron router-gateway-set demo-router ext-net")

def verify():
  print "[INFO] SKIP verify"

def main():
  createExternalNetwork()
  createTenantNetwork()
  verify()


if __name__ == '__main__':
  main()