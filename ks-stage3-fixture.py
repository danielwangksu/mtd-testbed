from model import *
from mongoengine import *

connect("fixture")

## Clear out collections
Instance.drop_collection()
Interface.drop_collection()

## Populate with test data
instance = Instance(hostname = "hornet01.mgmt.nw.com", tag = "apache2", status = "provisioned")
interface = Interface(instance = instance, name = "eth0", mac_address = "08:00:27:1e:4b:7c")

instance.save()
interface.save()

instance = Instance(hostname = "hornet02.mgmt.nw.com", tag = "apache2", status = "provisioned")
interface = Interface(instance = instance, name = "eth0", mac_address = "08:00:27:f8:60:b3")

instance.save()
interface.save()

instance = Instance(hostname = "hornet03.mgmt.nw.com", tag = "apache2", status = "provisioned")
interface = Interface(instance = instance, name = "eth0", mac_address = "08:00:27:6c:2a:25")

instance.save()
interface.save()