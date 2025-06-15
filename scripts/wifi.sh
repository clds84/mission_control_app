#!/bin/bash

echo connection name?
read connection_name
echo ssid?
read ssid
echo password?
read password
sudo nmcli c add type wifi con-name $connection_name ifname wlan0 ssid $ssid 
sleep 1
#echo password?
#read password
sudo nmcli c modify $connection_name wifi-sec.key-mgmt wpa-psk wifi-sec.psk $password
