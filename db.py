from mongoengine import *

###

class Switch(Document):
	switch_name = StringField(required=True)
	network     = StringField()
	netmask     = StringField()

class Interface(Document):
	interface_name = StringField(required=True)
	instance       = ReferenceField("Instance")
	mac_address    = StringField(required=True)
	ip_address     = StringField()
	switch         = ReferenceField(Switch)

class Instance(Document):
	hostname   = StringField(required=True)
	interfaces = ListField(ReferenceField(Interface))
	tag        = StringField(required=True)

###
