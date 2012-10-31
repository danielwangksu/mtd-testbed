from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

import config

webNo = 2
mailNo = 0
vpnNo = 0
clientNo = 1
logNo = 0
fileNo = 0

# Choose BluePrint (default BP1)

# connect to server
server = VIServer()
server.connect("192.168.1.15", "ian", "ccdc2013!")
print server.get_server_type()

# Host where the network will be created (first host) - in our case 192.168.1.142	
esxi_host = server.get_hosts().keys()[0] 

######################################### BluePrint 1 #########################################
# create vSwitches 
switch1Exists = False
if webNo or mailNo :
	switch1Exists = config.createSwitch("a-switch1", "a-switch1", 56, server, esxi_host)
	
switch2Exists = False
if vpnNo or clientNo or logNo or fileNo: 
	switch2Exists = config.createSwitch("a-switch2", "a-switch2", 56, server, esxi_host);
	
switch3Exists = False
if vpnNo or clientNo:
	switch3Exists = config.createSwitch("a-switch3", "a-switch3", 56, server, esxi_host);
	
switch4Exists = config.createSwitch("a-switch4", "a-switch4", 56, server, esxi_host);
	
# create pFW
template_vm = server.get_vm_by_name("mtd-debian-wheezy-64bits")
pFW = template_vm.clone("a-pFW",resourcepool = "resgroup-142")
	
if switch1Exists and switch2Exists:
	config.add_new_NIC(server, "a-pFW", "a-switch1")
	config.add_new_NIC(server, "a-pFW", "a-switch2")
elif switch1Exists and switch2Exists is False:
	config.add_new_NIC(server, "a-pFW", "a-switch1")
elif switch1Exists is False and switch2Exists:
	config.add_new_NIC(server, "a-pFW", "a-switch2")
else:
	print "There is no network behind the perimeter firewall"

# create intFW
template_vm = server.get_vm_by_name("mtd-debian-wheezy-64bits")
intFW = template_vm.clone("a-intFW",resourcepool = "resgroup-142")

if switch3Exists:
	config.add_new_NIC(server, "a-intFW", "a-switch2")
	config.add_new_NIC(server, "a-intFW", "a-switch3")
	config.add_new_NIC(server, "a-intFW", "a-switch4")
else:
	config.add_new_NIC(server, "a-intFW", "a-switch2")
	config.add_new_NIC(server, "a-intFW", "a-switch4")
	
# create controller
template_vm = server.get_vm_by_name("mtd-debian-wheezy-64bits")
controller = template_vm.clone("a-controller",resourcepool = "resgroup-142")

# create web server(s)
if webNo > 0:
	for i in range(0,webNo):
		template_vm = server.get_vm_by_name("mtd-debian-wheezy-64bits")
		webServer = template_vm.clone("a-web" + str(i),resourcepool = "resgroup-142")

# create client machines
if clientNo > 0:
	for i in range(0,clientNo):
		template_vm = server.get_vm_by_name("mtd-debian-wheezy-64bits")
		client = template_vm.clone("a-client" + str(i),resourcepool = "resgroup-142")

		#createVM($fh, "a-web$i", "mtd-webServerTemplate", 1, server);
		#$serverArray[] = "a-web$i";
		
###############################################################################################
'''
# Clone VM
test_vm = server.get_vm_by_name("cdc2-heisenberg")
new_vm = test_vm.clone("mtd-clone_test")

# Clone (deploy) from template
template_vm = server.get_vm_by_name("mtd-intFW")
new_vm1 = template_vm.clone("mtd-#clone_from_template",resourcepool = "resgroup-142")
'''

'''Add new virtual switch
#Get the first host system 
host_system = server.get_hosts().keys()[0] 
prop = VIProperty(server, host_system) 

#print existing virtual switchs 
for vs in prop.configManager.networkSystem.networkInfo.vswitch: 
    print vs.name 

#print NIC keys 
for pnic in prop.configManager.networkSystem.networkInfo.pnic: 
   print pnic.key 

network_system = prop.configManager.networkSystem._obj 
vswitch_name = "My super switch2222" 
num_ports = 56 

#I'm commenting the bridge_nic parameter, because it will fail 
#if the given nic is used in another vswitch, check if it works 
#for you when providing an available physical nic 

config.add_virtual_switch(server, network_system, vswitch_name, num_ports) #, bridge_nic=nic) 

#Add a port group 
vlan_id = 0 
config.add_port_group(server, network_system, vswitch_name, vlan_id, vswitch_name) 
'''

#config.add_new_NIC(server, "BT5R2", "a-switch3")

#config.getMAC(server, "a-pFW")

