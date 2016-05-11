#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *


def createHeat():
  Task("mkdir -p ../tmp")

  f = FileCopy("../lib/heat/create_heat.sh", "../tmp/create_heat.sh")
  f.replace('MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])
  f.replace('HEAT_DBPASS', User.HEAT[User.PASSWORD])
  f.exe()

  Source().admin()
  Task("openstack user create --password " + User.HEAT[User.PASSWORD] + " heat")
  Task("openstack role add --project service --user heat admin")
  Task("openstack role create heat_stack_owner")
  Task("openstack role add --project demo --user demo heat_stack_owner")
  Task("openstack role create heat_stack_user")
  Task("openstack service create --name heat \
          --description 'Orchestration' orchestration")
  Task("openstack service create --name heat-cfn \
          --description 'Orchestration'  cloudformation")
  Task("openstack endpoint create \
          --publicurl http://controller:8004/v1/%\(tenant_id\)s \
          --internalurl http://controller:8004/v1/%\(tenant_id\)s \
          --adminurl http://controller:8004/v1/%\(tenant_id\)s \
          --region RegionOne \
          orchestration")
  Task("openstack endpoint create \
          --publicurl http://controller:8000/v1 \
          --internalurl http://controller:8000/v1 \
          --adminurl http://controller:8000/v1 \
          --region RegionOne \
          cloudformation")

def installHeat():
  yumInstall("openstack-heat-api")
  yumInstall("openstack-heat-api-cfn")
  yumInstall("openstack-heat-engine")
  yumInstall("python-heatclient")

  f = FileCopy("../lib/heat/heat-dist.conf", "/etc/heat/heat.conf")
  f.replace('HEAT_DBPASS', User.HEAT[User.PASSWORD])
  f.replace('HEAT_PASS', User.HEAT[User.PASSWORD])
  f.replace('HEAT_DOMAIN_PASS', User.HEAT[User.PASSWORD])
  f.replace('RABBIT_PASS', User.RABBITMQ[User.PASSWORD])

  Task("chown -R heat:heat /etc/heat/heat.conf")

  Source().admin()
  Task("heat-keystone-setup-domain \
          --stack-user-domain-name heat_user_domain \
          --stack-domain-admin heat_domain_admin \
          --stack-domain-admin-password " + User.HEAT[User.PASSWORD])
  Task("su -s /bin/sh -c 'heat-manage db_sync' heat")

  Systemctl("openstack-heat-api.service", ["enable", "start"])
  Systemctl("openstack-heat-api-cfn.service", ["enable", "start"])
  Systemctl("openstack-heat-engine.service", ["enable", "start"])

def verify():
  Source().admin()
  Task("mkdir -p ../tmp")
  
  f = FileCopy("../lib/heat/test-stack.yml", "../tmp/test-stack.yml")
  Task("NET_ID=$(nova net-list | awk '/ demo-net / { print $2 }')")
  Task("heat stack-create -f " + f.dst() + " \
          -P 'ImageID=cirros-0.3.4-x86_64;NetID=$NET_ID' testStack")
  Task("heat stack-list")

def main():
  createHeat()
  installHeat()
  
  verify()


if __name__ == '__main__':
  main()