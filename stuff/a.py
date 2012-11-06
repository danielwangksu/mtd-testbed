from db import *

connect("blueprint4")

switch = Switch(switch_name="a-switch2")
instance = Instance(hostname = "a-pFW0", tag = "pFW")
interface = Interface(interface_name = "eth0", instance = instance,mac_address = "11:22:33:44:55:66")
interface1 = Interface(interface_name = "eth1", instance = instance, mac_address = "99:22:33:44:55:66")
instance.interfaces.append(interface)
instance.interfaces.append(interface1)

switch.save()
#interface.save()
#interface1.save()
#instance.save()
instance.cascade_save()

print instance.hostname

for i in instance.interfaces:
	print i.interface_name

print interface.instance.hostname
print interface1.instance.hostname
