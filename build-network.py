from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

from model import *
from util import *
from util_db import *

webNo  = 2
mailNo = 0
vpnNo  = 0
clientNo = 1
logNo    = 0
fileNo   = 0

# Choose BluePrint (default BP1)

# connect to server
server = VIServer()
server.connect("192.168.1.15", "ian", "ccdc2013!")
connect("vm_db")
print server.get_server_type()

# Host where the network will be created (first host) - in our case 192.168.1.142	
esxi_host = server.get_hosts().keys()[0] 

################################################# BluePrint 1 ##############################################
# create vSwitches 
switch1Exists = False
if webNo or mailNo :
	switch1Exists = create_switch("a-switch1", "a-switch1", 56, server, esxi_host)
	switch1 = Switch(name = "a-switch1", network = "172.17.1.0", netmask = "255.255.255.0")
	switch1.save()
	
switch2Exists = create_switch("a-switch2", "a-switch2", 56, server, esxi_host);
switch2 = Switch(name="a-switch2", network = "172.17.2.0", netmask = "255.255.255.0")
switch2.save()

switch3Exists = False
if vpnNo or clientNo:
	switch3Exists = create_switch("a-switch3", "a-switch3", 56, server, esxi_host);
	switch3 = Switch(name="a-switch3", network = "172.17.3.0", netmask = "255.255.255.0")
	switch3.save()

switch4Exists = create_switch("a-switch4", "a-switch4", 56, server, esxi_host);
switch4 = Switch(name="a-switch4", network = "172.17.4.0", netmask = "255.255.255.0")
switch4.save()

network1 = 2
network3 = 2
network4 = 2
# create pFW
create_VMs (server, 1, 0, "pFW", switch1, "mtd-mgmt", switch2, switch3, switch4)

# create intFW
create_VMs (server, 1, 0, "intFW", switch1, "mtd-mgmt", switch2, switch3, switch4)

# create web server(s)
if webNo > 0:
	create_VMs (server, webNo, network1, "web", switch1)
	network1 = network1 + webNo

# create mail server(s)
if mailNo > 0:
	create_VMs (server, mailNo, network1, "mail", switch1) 
	network1 = network1 + mailNo

# create client machines
if clientNo > 0:
	create_VMs (server, clientNo, network3, "client", switch3)
	network3 = network3 + clientNo

# create VPN server(s)
if vpnNo > 0:
	create_VMs (server, vpnNo, network3, "vpn", switch3)
	network3 = network3 + vpnNo

# create log server(s)
if logNo > 0:
	create_VMs (server, logNo, network4, "log", switch4)
	network4 = network4 + logNo

# create file server(s)
if fileNo > 0:
	create_VMs (server, fileNo, network4, "file", switch4)
	network4 = network4 + fileNo

############################################################################################################

