#!/bin/bash
echo Do you need to set up WiFi connection to Raspberry Pi? y/n 
read con
if [ $con == n ]
  then
    ip_address=$(ping raspberrypi -c1 | head -1 | grep -Eo '[0-9.]{4,}')   
    ssh pi@$ip_address  
  else 
    echo Have you plugged your SD-card into your laptop? y/n
    read sd_card
    if [ $sd_card == y ]
      then
        echo Your WiFi Network name: 
        read wifi_net
        echo Your WiFi Password: 
        read wifi_pas
        rm -f /Volumes/boot/wpa_supplicant.conf
        touch /Volumes/boot/wpa_supplicant.conf
    
        echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US
network={
    ssid=\"$wifi_net\"
    psk=\"$wifi_pas\"
    scan_ssid=1
}" >> /Volumes/boot/wpa_supplicant.conf
	rm -f /Volumes/boot/ssh
        touch /Volumes/boot/ssh
        echo WiFi set up done, please insert SD-card into the Raspberry Pi and connect it to the laptop \(press ENTER when done\)
        exit 

    else 
      echo Plug your SD-card and run again
      exit
  fi 
fi