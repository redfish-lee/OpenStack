# Openstack Kilo Scripts
CentOS Openstack Kilo [Document][1]

## Before
### Virturl Box
open two NAT before installation

## Intallation
### pull
get python script files from github

```sh
git clone https://github.com/aaaa1379/OpenStack.git
cd OpenStack/centos-kilo/src
```

### basic
in the `OpenStack/centos-kilo/src` and complete the following commands

```sh
python basicEnv.py
# press 'y' for reboot
python keystone.py
python glance.py
python nova.py
python neutron.py
python network.py
python horizon.py
# press 'y' for reboot
```

### options
you can execute after basic installation

```sh
python heat.py
python ceilometer.py
```

[1]: http://docs.openstack.org/kilo/install-guide/install/yum/content/

