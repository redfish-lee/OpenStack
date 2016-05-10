#!/usr/bin/python
# -*- coding: UTF-8 -*-

from config import *
from func import *

def createKeystone():
  Task("mkdir -p ../tmp")

  f = FileCopy("../lib/glance/create_keystone.sh", "../tmp/create_keystone.sh")
  f.replace('MYSQL_PASSWORD', User.MYSQL[User.PASSWORD])
  f.replace('KEYSTONE_DBPASS', User.GLANCE[User.PASSWORD])
  f.exe()

def installKeystone():
  install_list = [
    "openstack-keystone",
    "httpd",
    "mod_wsgi",
    "python-openstackclient",
    "memcached",
    "python-memcached",
  ]

  yumInstall(install_list)

  Systemctl("memcached.service", ["enable", "start"])

  f = FileCopy("../lib/glance/keystone.conf", "/etc/keystone/keystone.conf")
  f.replace('ADMIN_TOKEN', User.ADMIN[User.PASSWORD])
  f.replace('KEYSTONE_DBPASS', User.GLANCE[User.PASSWORD])

  Task("/bin/sh -c 'keystone-manage db_sync' keystone")

def configureHTTP():

  FileCopy("../lib/glance/httpd.conf", "/etc/httpd/conf/httpd.conf")
  FileCopy("../lib/glance/wsgi-keystone.conf", "/etc/httpd/conf.d/wsgi-keystone.conf")

  # curl http://git.openstack.org/cgit/openstack/keystone/plain/httpd/keystone.py?h=stable/kilo \
  # | tee /var/www/cgi-bin/keystone/main /var/www/cgi-bin/keystone/admin
  Task("mkdir -p /var/www/cgi-bin/keystone")
  FileCopy("../lib/glance/cgi-bin_keystone", "/var/www/cgi-bin/keystone/main")
  FileCopy("../lib/glance/cgi-bin_keystone", "/var/www/cgi-bin/keystone/admin")

  Task("chown -R keystone:keystone /var/www/cgi-bin/keystone")
  Task("find /opt/lampp/htdocs -type d -exec chmod 755 {} \;")

  Systemctl("httpd.service", ["enable", "start"])

def endPoint():
  Source.export("OS_TOKEN", User.ADMIN[User.PASSWORD])
  Source.export("OS_URL",   'http://controller:35357/v2.0')
  Task("openstack service create \
          --name keystone --description 'OpenStack Identity' identity")
  Task("openstack endpoint create \
          --publicurl http://controller:5000/v2.0 \
          --internalurl http://controller:5000/v2.0 \
          --adminurl http://controller:35357/v2.0 \
          --region RegionOne \
          identity")

def createUser():
  # Admin
  Task("openstack project create --description 'Admin Project' admin")
  Task("openstack user create --password " + User.ADMIN[User.PASSWORD] + " admin")
  Task("openstack role create admin")
  Task("openstack role add --project admin --user admin admin")

  Task("openstack project create --description 'Service Project' service")

  # Demo
  Task("openstack project create --description 'Demo Project' demo")
  Task("openstack user create --password " + User.DEMO[User.PASSWORD] + " demo")
  Task("openstack role create user")
  Task("openstack role add --project demo --user demo user")

def verify():
  # /usr/share/keystone/keystone-dist-paste.ini
  FileCopy("../lib/glance/keystone-dist-paste.ini","/usr/share/keystone/keystone-dist-paste.ini")
  Source.delexp("OS_TOKEN")
  Source.delexp("OS_URL")
  # step 3
  Task("openstack --os-auth-url http://controller:35357 \
          --os-project-name admin --os-username admin --os-password " + User.ADMIN[User.PASSWORD] \
          + "token issue")
  Task("openstack --os-auth-url http://controller:35357 \
          --os-project-domain-id default --os-user-domain-id default \
          --os-project-name admin --os-username admin --os-password " + User.ADMIN[User.PASSWORD] \
          + "token issue")
  Task("openstack --os-auth-url http://controller:35357 \
          --os-project-name admin --os-username admin --os-password " + User.ADMIN[User.PASSWORD] \
          + "project list")
  Task("openstack --os-auth-url http://controller:35357 \
          --os-project-name admin --os-username admin --os-password " + User.ADMIN[User.PASSWORD] \
          + "user list")
  Task("openstack --os-auth-url http://controller:35357 \
          --os-project-name admin --os-username admin --os-password " + User.ADMIN[User.PASSWORD] \
          + "role list")
  # step 8
  Task("openstack --os-auth-url http://controller:5000 \
          --os-project-domain-id default --os-user-domain-id default \
          --os-project-name demo --os-username demo --os-password " + User.DEMO[User.PASSWORD] \
          + "token issue")

def scripts():
  f = FileCopy("../lib/glance/admin-openrc.sh","~/admin-openrc.sh")
  f.replace('ADMIN_TOKEN', User.ADMIN[User.PASSWORD])
  f = FileCopy("../lib/glance/demo-openrc.sh", "~/demo-openrc.sh")
  f.replace('DEMO_PASS', User.DEMO[User.PASSWORD])
  Source.admin()
  Task("openstack token issue")

def main():
  """Install and configure"""
  createKeystone()
  installKeystone()
  configureHTTP()

  """Create the service entity and API endpoint"""
  endPoint()

  """Create projects, users, and roles"""
  createUser()

  """Verify operation"""
  verify()

  """Create OpenStack client environment scripts"""
  scripts()


if __name__ == '__main__':
  main()