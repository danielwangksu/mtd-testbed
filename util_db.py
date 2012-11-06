from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

from util import *
from db import *

def storeInfo_inDB(server, vm_name, tag, switch1, switch2 = None, switch3 = None, switch4 = None):
	"""Stores MAC and interface names to DB

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string
	"""
	instance = Instance(hostname = vm_name, tag = tag)
	instance.save()
	vm = server.get_vm_by_name(vm_name)

	for id, device in vm.get_property("devices").items():
		if device.has_key("macAddress"):
			if str(device["label"]) == "Network adapter 1":
				switch = switch1
			if str(device["label"]) == "Network adapter 2":
				switch = switch2
			if str(device["label"]) == "Network adapter 3":
				switch = switch3
			if str(device["label"]) == "Network adapter 4":
				switch = switch4
			interface = Interface(interface_name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]), switch = switch)
			interface.save()
			instance.interfaces.append(interface)
			instance.save()
