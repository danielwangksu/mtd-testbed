from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

from util import *
from model import *

def storeInfo_inDB(server, vm_name, tag, switch1, switch2 = None, switch3 = None, switch4 = None, ip = None, gateway = None):
	"""Stores MAC and interface names in the DB

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string
	"""
	instance = Instance(hostname = vm_name, tag = tag, status = "provisioned")
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

			interface = Interface(name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]), ip_address = ip, network = str(switch.network), netmask = str(switch.netmask), gateway = gateway, switch = switch)
			interface.save()
			instance.interfaces.append(interface)
			instance.save()

def storeFW_inDB(server, vm_name, tag, switch1, switch2 = None, switch3 = None, switch4 = None):
	"""Stores FW MAC(s) and interface(s) names in the DB

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string
	"""
	instance = Instance(hostname = vm_name, tag = tag, status = "provisioned")
	instance.save()
	vm = server.get_vm_by_name(vm_name)

	if tag == "pFW":
		for id, device in vm.get_property("devices").items():
			if device.has_key("macAddress"):
				if str(device["label"]) == "Network adapter 1":
					interface = Interface(name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]))
					interface.save()
					instance.interfaces.append(interface)

				if str(device["label"]) == "Network adapter 2":
					interface = Interface(name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]),ip_address = "172.17.2.1", network = "172.17.2.0", netmask = "255.255.255.0", switch = switch2)
					interface.save()
					instance.interfaces.append(interface)

				if str(device["label"]) == "Network adapter 3":
					interface = Interface(name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]),ip_address = "172.17.1.1", network = "172.17.1.0", netmask = "255.255.255.0", switch = switch1)
					interface.save()
					instance.interfaces.append(interface)

	if tag == "intFW":
		for id, device in vm.get_property("devices").items():
			if device.has_key("macAddress"):
				if str(device["label"]) == "Network adapter 1":
					interface = Interface(name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]),ip_address = "172.17.2.2", network = "172.17.2.0", netmask = "255.255.255.0", gateway = "172.17.2.1", switch = switch2)
					interface.save()
					instance.interfaces.append(interface)

				if str(device["label"]) == "Network adapter 2":
					interface = Interface(name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]),ip_address = "172.17.4.1", network = "172.17.4.0", netmask = "255.255.255.0", switch = switch4)
					interface.save()
					instance.interfaces.append(interface)

				if str(device["label"]) == "Network adapter 3":
					interface = Interface(name = str(device["label"]), instance = instance, mac_address = str(device["macAddress"]),ip_address = "172.17.3.1", network = "172.17.3.0", netmask = "255.255.255.0", switch = switch3)
					interface.save()
					instance.interfaces.append(interface)					
		

	instance.save()
