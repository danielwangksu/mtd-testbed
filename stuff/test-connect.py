from mongoengine import *

###
class Instance(Document):
	hostname = StringField(required=True)
	tag = StringField(required=True)

class Switch(Document):
	switch_name = StringField(required=True)
	network = StringField()
	netmask = StringField()

class Interface(Document):
	interface_name = StringField(required=True)
	instance = Instance
	mac_address = StringField(required=True)
	ip_address = StringField()
	switch = Switch

###

connect("blueprint1")

inst = Instance(hostname = "a-pFW0", tag = "pFW" )
swi = Switch(switch_name="a-switch1")

inter = Interface(interface_name = "eth0", instance = inst, mac_address = "11:00:00:00:00:00", switch = swi)

inst.save()
swi.save()
inter.save()

print inter.instance.hostname
print inter.instance.tag
print inter.switch.switch_name

