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
connect("update_db")

# if the db exists, delete previous records stored in the db
Instance.drop_collection()
Interface.drop_collection()
Switch.drop_collection()


# Host where the network will be created (first host) - in our case 192.168.1.142	
esxi_host = server.get_hosts().keys()[0] 

# Customized for Blueprint1 
# Assuming all VMs and vSwitches start with "a-" and there are >9 VMs of the same type

lab_switch = Switch(name = "N127 Physical Network", network = "192.168.1.0", netmask = "255.255.255.0")
lab_switch.save()

print "\nLooking for vSwitches ..."
prop = VIProperty(server, esxi_host) 
for vs in prop.configManager.networkSystem.networkInfo.vswitch:
	if vs.name == "a-switch1":  
		switch1 = Switch(name = vs.name, network = "172.17.1.0", netmask = "255.255.255.0")
		switch1.save() 
		print vs.name + " found and stored in the database"
		network1_counter = 2

	if vs.name == "a-switch2": 
		switch2 = Switch(name = vs.name, network = "172.17.2.0", netmask = "255.255.255.0")
		switch2.save() 
		print vs.name + " found and stored in the database"

	if vs.name == "a-switch3":
		switch3 = Switch(name = vs.name, network = "172.17.3.0", netmask = "255.255.255.0")
		switch3.save()
		print vs.name + " found and stored in the database"
		network3_counter = 2

	if vs.name == "a-switch4":
		switch4 = Switch(name = vs.name, network = "172.17.4.0", netmask = "255.255.255.0")
		switch4.save() 
		print vs.name + " found and stored in the database"
		network4_counter = 2

vmlist = server.get_registered_vms()
print "\nFound VM(s): "
vm_name = ""
for vm in vmlist:
	vm_dir = vm.split('/')[1]
	if vm_dir.split('.')[0][:2] == "a-":
		vm_name = vm_dir.split('.')[0]
		print vm_name

		vm_type = vm_name[2:][:-1]

		if vm_type == "web" or vm_type == "mail":
			genIP(server, vm_name, network1_counter, vm_type, switch1)
			network1_counter = network1_counter + 1
	
		if vm_type== "a-vpn" or vm_type == "client":
			genIP(server, vm_name, network3_counter, vm_type, switch3)
			network3_counter = network3_counter + 1

		if vm_type == "log" or vm_type == "file":
			genIP(server, vm_name, network4_counter, vm_type, switch4)
			network3_counter = network4_counter + 1

		if vm_type == "pFW":
			storeFW_inDB(server, "a-pFW0", vm_type, switch1, switch2, switch3, switch4, lab_switch)

		if vm_type == "intFW":
			storeFW_inDB(server, "a-intFW0", vm_type, switch1, switch2, switch3, switch4)

####### Simulating that VMs are configured #######
for instance in Instance.objects:
	instance.status = "configured"
##################################################

while(True):
	print "\nVM(s) Status:"
	for instance in Instance.objects:
		print instance.hostname + " Status: \'" + instance.status + "\' #_of_NICs: " + str(len(instance.interfaces))
		if instance.status == "configured":
			count = 1
			for interface in instance.interfaces:
								
				deploy_VM(server, instance.hostname, instance.tag, interface.name, interface.mac_address, interface.switch.name)

				if count is len(instance.interfaces):
					instance.status = "deployed"
					instance.save(cascade = True)
				else:
					count = count + 1
	
	time.sleep(5)


