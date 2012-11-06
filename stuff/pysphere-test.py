from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

from util import *
from db import *
from util_db import *

# connect to server
server = VIServer()
server.connect("192.168.1.15", "ian", "ccdc2013!")
print server.get_server_type()
connect("vm_db1")

swi1 = Switch(switch_name="a-switch1")
swi2 = Switch(switch_name="a-switch2")
swi3 = Switch(switch_name="a-switch3")
swi4 = Switch(switch_name="a-switch4")
swi1.save()
swi2.save()
swi3.save()

storeInfo_inDB(server, "a-intFW0", "intFW", swi1, swi2, swi3, swi4)



'''
instance = Instance(hostname = "a-pFW0", tag = "pFW")
interface = Interface(interface_name = "eth0", instance = instance,mac_address = "11:22:33:44:55:66")
interface1 = Interface(interface_name = "eth1", instance = instance, mac_address = "99:22:33:44:55:66")
instance.interfaces.append(interface)
instance.interfaces.append(interface1)
'''
#get_mac_addresses(server, "a-pFW0")



#template_vm = server.get_vm_by_name("mtd-base-debian-wheezy")
#test_vm = template_vm.clone("a-test", resourcepool = "resgroup-142")

#create_nic(server, "a-test", "mtd-mgmt")


#reconfigure_nic(server, "a-pFW", "00:50:56:bc:2f:06", "a-switch1")

'''
# Clone VM
test_vm = server.get_vm_by_name("cdc2-heisenberg")
new_vm = test_vm.clone("mtd-clone_test")

# Clone (deploy) from template
template_vm = server.get_vm_by_name("mtd-intFW")
new_vm1 = template_vm.clone("mtd-#clone_from_template", resourcepool = "resgroup-142")
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

add_virtual_switch(server, network_system, vswitch_name, num_ports) #, bridge_nic=nic) 

#Add a port group 
vlan_id = 0 
add_port_group(server, network_system, vswitch_name, vlan_id, vswitch_name) 
'''

#create_nic(server, "BT5R2", "a-switch3")

#get_mac(server, "a-pFW")

'''if switch1Exists and switch2Exists:
	create_nic(server, "a-pFW", "mtd-mgmt")
	create_nic(server, "a-pFW", "mtd-mgmt")
elif switch1Exists or switch2Exists:
	create_nic(server, "a-pFW", "mtd-mgmt")
else:
	print "There is no network behind the perimeter firewall"'''

'''if switch3Exists:
	create_nic(server, "a-intFW", "mtd-mgmt")
	create_nic(server, "a-intFW", "mtd-mgmt")
else:
	create_nic(server, "a-intFW", "mtd-mgmt")'''

