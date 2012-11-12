from model import *
from mongoengine import *

connect("fixture")

instance = Instance(hostname = "flame01.mgmt.nw.com", tag = "apache2")
interface = Interface(instance = instance, interface_name="eth0", mac_address="08:00:27:b4:10:c6")

instance.save()
interface.save()
# instance.cascade_save()
