#!/usr/bin/expect --

## for centos 7 kilo openstack
spawn /usr/bin/mysql_secure_installation

expect "Enter current password for root (enter for none):"
send "\r"

expect "Set root password?"
send "y\r"

expect "New password:"
send "MYSQL_PASSWORD\r"

expect "Re-enter new password:"
send "MYSQL_PASSWORD\r"

expect "Remove anonymous users?"
send "y\r"

expect "Disallow root login remotely?"
send "y\r"

expect "Remove test database and access to it?"
send "y\r"

expect "Reload privilege tables now?"
send "y\r"

puts "Ended expect script."