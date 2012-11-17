from mongoengine import *

###

class Switch(Document):
	name        = StringField(required=True)
	network     = StringField()
	netmask     = StringField()

class Interface(Document):
	name           = StringField(required=True)
	instance       = ReferenceField("Instance", dbref = False)
	mac_address    = StringField(required=True)
	ip_address     = StringField()
	network		   = StringField()
	netmask		   = StringField()
	gateway		   = StringField()
	switch         = ReferenceField(Switch, dbref = False)

class Instance(Document):
	hostname   = StringField(required=True)
	interfaces = ListField(ReferenceField(Interface, dbref = False))
	tag        = StringField(required=True)
	status	   = StringField(required=True)

###
