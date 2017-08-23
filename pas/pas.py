import subprocess
import time
import os
log = time.strftime("/home/pi/pas/log/%Y%m%d-%H%M%S")
subprocess.Popen(["sudo","ettercap","-Tq", "-i", "eth0", "-L", log])
time.sleep(10)
os.system('sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"')

