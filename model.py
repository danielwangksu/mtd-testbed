from mongoengine import *

###

class Switch(Document):
	name        = StringField(required=True)
	network     = StringField()
	netmask     = StringField()

class Interface(Document):
	name           = StringField(required=True)
	instance       = ReferenceField("Instance")
	mac_address    = StringField(required=True)
	ip_address     = StringField()
	network		   = StringField()
	netmask		   = StringField()
	gateway		   = StringField()
	switch         = ReferenceField(Switch)

class Instance(Document):
	hostname   = StringField(required=True)
	interfaces = ListField(ReferenceField(Interface))
	tag        = StringField(required=True)
	status	   = StringField(required=True)

###
