from mongoengine import *

###

class Interface(Document):
    name = StringField(required=True)
    mac_address = StringField(required=True)
    ip_address = StringField()

class Instance(Document):
    hostname = StringField(required=True)
    interfaces = ListField(ReferenceField(Interface))

###

connect("blueprint")

interface = Interface(name = "eth0", mac_address = "00:00:00:00:00:00")

instance = Instance(hostname = "firefly01")
instance.interfaces.append(interface)

interface.cascade_save()