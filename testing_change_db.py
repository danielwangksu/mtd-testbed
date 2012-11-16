import time
from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

from model import *
from util import *
from util_db import *

# connect to server
server = VIServer()
server.connect("192.168.1.15", "ian", "ccdc2013!")
print "\nConnected to:" + server.get_server_type()

# connect to DB
connect("vm_db")

for instance in Instance.objects:
	print instance.hostname + " - " + instance.status

for instance in Instance.objects:
	instance.status = "configured"
	instance.save()

for instance in Instance.objects:
	print instance.hostname + " - " + instance.status

powerON(server,"pFW")
powerON(server,"intFW")
powerON(server,"web")
powerON(server,"mail")
powerON(server,"log")
powerON(server,"file")
powerON(server,"vpn")
powerON(server,"client")


