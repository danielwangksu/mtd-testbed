from model import *
from mongoengine import *

connect("fixture")

## Clear out collections
Instance.drop_collection()
Interface.drop_collection()

## Populate with test data
instance = Instance(hostname = "hornet01.mgmt.nw.com", tag = "apache2", status = "provisioned")
interface = Interface(instance = instance, name = "eth0", mac_address = "08:00:27:b4:10:c6")

instance.save()
interface.save()