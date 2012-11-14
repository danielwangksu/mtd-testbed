from pysphere import *
from pysphere.resources import VimService_services as VI

from util_db import *

def create_nic(server, vm_name, network_name, run_async = False):
	"""Adds a new NIC to an existing VM

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string
	@network_name: netork name string"""

	vm = server.get_vm_by_name(vm_name)
	if not vm:
	    raise Exception("VM %s not found" % vm_name)

	#Invoke ReconfigVM_Task
	request = VI.ReconfigVM_TaskRequestMsg()
	_this = request.new__this(vm._mor)
	_this.set_attribute_type(vm._mor.get_attribute_type())
	request.set_element__this(_this)
	spec = request.new_spec()
	# Add a NIC; the network name must be set as the device name
	dev_change = spec.new_deviceChange()
	dev_change.set_element_operation("add")
	nic_ctlr = VI.ns0.VirtualE1000_Def("nic_ctlr").pyclass()
	nic_backing = VI.ns0.VirtualEthernetCardNetworkBackingInfo_Def("nic_backing").pyclass()
	nic_backing.set_element_deviceName(network_name)
	nic_ctlr.set_element_addressType("generated")
	nic_ctlr.set_element_backing(nic_backing)
	nic_ctlr.set_element_key(4)
	dev_change.set_element_device(nic_ctlr)

	spec.set_element_deviceChange([dev_change])
	request.set_element_spec(spec)
	ret = server._proxy.ReconfigVM_Task(request)._returnval

	if not run_async:
		# Wait for the task to finish
		task = VITask(ret, server)
		status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
		if status == task.STATE_SUCCESS:
			print "VM %s successfully reconfigured" % vm_name
		
		elif status == task.STATE_ERROR:
			print "Error reconfiguring vm: %s" % vm_name, task.get_error_message()

def reconfigure_nic(server, vm_name, mac_address, network_name, run_async = False):
	"""Reconfigures a NIC by its MAC address
	
	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	
	@vm_name: vm name string
	@mac_address: MAC address of the target NIC
	@network_name: network name string"""
		
	vm = server.get_vm_by_name(vm_name) 
	
	if not vm:
	        raise Exception("VM %s not found" % vm_name)
	
	# Find Virtual Nic device 
	net_device = None 
	for dev in vm.properties.config.hardware.device: 
	    if dev._type in ["VirtualE1000", "VirtualE1000e", 
	                     "VirtualPCNet32", "VirtualVmxnet"] and dev.macAddress == mac_address: 
	        net_device = dev._obj 
	        break 
	
	if not net_device: 
	    raise Exception("The vm seems to lack a Virtual Nic") 
	        
	# Set NIC MAC address to Manual and set address 
	# net_device.set_element_addressType("Manual") 
	net_device.Backing.set_element_deviceName(network_name)
	# Invoke ReconfigVM_Task 
	request = VI.ReconfigVM_TaskRequestMsg() 
	_this = request.new__this(vm._mor) 
	_this.set_attribute_type(vm._mor.get_attribute_type()) 
	request.set_element__this(_this) 
	spec = request.new_spec() 
	dev_change = spec.new_deviceChange() 
	dev_change.set_element_device(net_device) 
	dev_change.set_element_operation("edit") 
	spec.set_element_deviceChange([dev_change]) 
	request.set_element_spec(spec) 
	ret = server._proxy.ReconfigVM_Task(request)._returnval 
	
	# Wait for the task to finish 
	if not run_async:
		task = VITask(ret, server) 
		status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR]) 
		if status == task.STATE_SUCCESS: 
			print "VM %s successfully reconfigured" % vm_name 
		elif status == task.STATE_ERROR: 
			print "Error reconfiguring vm_name: %s" % vm_name, task.get_error_message() 

def delete_vm(server, vm_name, run_async = False):
	"""Deletes a VM from the disk

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string"""
	#Get VM
	vm = server.get_vm_by_name(vm_name)

	vm.power_off()

	#Invoke Destroy_Task
	request = VI.Destroy_TaskRequestMsg()
	_this = request.new__this(vm._mor)
	_this.set_attribute_type(vm._mor.get_attribute_type())
	request.set_element__this(_this)
	ret = server._proxy.Destroy_Task(request)._returnval

	#Wait for the task to finish
	if not run_async:
		task = VITask(ret, server)
	
		status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
		if status == task.STATE_SUCCESS:
			print "VM successfully deleted from disk"
		elif status == task.STATE_ERROR:
			print "Error removing vm:", task.get_error_message() 

def get_mac_addresses(server, vm_name):
	"""Get MAC addresses for each interface on a VM

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string
	"""

	vm = server.get_vm_by_name(vm_name)

	for id, device in vm.get_property("devices").items():
		if device.has_key("macAddress"):
			print device["label"] + " - " +device["macAddress"] 

def add_virtual_switch(server, network_system, name, num_ports, bridge_nic = None, mtu = None):
	"""Add a new vSwitch

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@network_system: network_sys object of a specific esxi host
	@name: vSwitch name
	@num_ports: number of ports
	"""
	request = VI.AddVirtualSwitchRequestMsg() 
	_this = request.new__this(network_system) 
	_this.set_attribute_type(network_system.get_attribute_type()) 
	request.set_element__this(_this) 
	request.set_element_vswitchName(name) 

	spec = request.new_spec() 
	spec.set_element_numPorts(num_ports + 8) 

	if isinstance(mtu, int): 
		spec.set_element_mtu(mtu) 

	if bridge_nic: 
		bridge = VI.ns0.HostVirtualSwitchSimpleBridge_Def("bridge").pyclass() 
		bridge.set_element_nicDevice(bridge_nic) 
		spec.set_element_bridge(bridge) 

	request.set_element_spec(spec) 
	server._proxy.AddVirtualSwitch(request) 

def add_port_group(server, network_system, name, vlan_id, vswitch):
	"""Add a new port group to a vSwitch

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@network_system: network_sys object of a specific esxi host
	@name: port group name
	@vlan_id: VLAN ID, 0 - none
	@vswitch: vSwitch name
	"""
	request = VI.AddPortGroupRequestMsg() 
	_this = request.new__this(network_system) 
	_this.set_attribute_type(network_system.get_attribute_type()) 
	request.set_element__this(_this) 

	portgrp = request.new_portgrp() 
	portgrp.set_element_name(name) 
	portgrp.set_element_vlanId(vlan_id) 
	portgrp.set_element_vswitchName(vswitch) 
	portgrp.set_element_policy(portgrp.new_policy()) 
	request.set_element_portgrp(portgrp) 

	server._proxy.AddPortGroup(request) 

def create_switch(vswitch_name, port_group_name, num_ports, server, esxi_host): 
	prop = VIProperty(server, esxi_host)
	network_system = prop.configManager.networkSystem._obj 
	
	# Create vSwitch
	add_virtual_switch(server, network_system, vswitch_name, num_ports) 

	# Add a port group 
	vlan_id = 0 
	add_port_group(server, network_system, vswitch_name, vlan_id, vswitch_name) 

	return True

def create_VMs (server, no, counter, vm_type, switch1, network = None, switch2 = None, switch3 = None, switch4 = None, template_name = "mtd-base-debian-wheezy", pool = "resgroup-142"):
	for i in range(0,no):
		template_vm = server.get_vm_by_name(template_name)
		vm_name = "a-"+ vm_type + str(i)
		vm = template_vm.clone(vm_name, resourcepool = pool)

		if vm_type == "web" or vm_type == "mail" :
			ip = "172.17.1." + str(counter)
			storeInfo_inDB(server, vm_name, vm_type, switch1, switch2, switch3, switch4, ip, gateway = "172.17.1.1")
			counter = counter + 1

		if vm_type == "client" or vm_type == "vpn" :
			ip = "172.17.3." + str(counter)
			storeInfo_inDB(server, vm_name, vm_type, switch1, switch2, switch3, switch4, ip, gateway = "172.17.3.1")
			counter = counter + 1

		if vm_type == "log" or vm_type == "file" :
			ip = "172.17.4." + str(counter)
			storeInfo_inDB(server, vm_name, vm_type, switch1, switch2, switch3, switch4, ip, gateway = "172.17.4.1")
			counter = counter + 1

		get_mac_addresses(server, vm_name)
	
	if vm_type == "pFW" and no is 1:
		configFW_NIC(server, "a-pFW0", network, switch1, switch2, switch3, switch4)

	if vm_type == "intFW" and no is 1:
		configFW_NIC(server, "a-intFW0", network, switch1, switch2, switch3, switch4)

def configFW_NIC(server, name, network, switch1 = None, switch2 = None, switch3 = None, switch4 = None):
	if name == "a-pFW0":
		if switch1 and switch2:
			create_nic(server, name, network)
			create_nic(server, name, network)
			storeFW_inDB(server, name, "pFW", switch1, switch2, switch3, switch4)
		elif switch1 or switch2:
			create_nic(server, name, network)
			storeFW_inDB(server, name, "pFW", switch1, switch2, switch3, switch4)
		else:
			print "There is no network behind the perimeter firewall"
	
	if name == "a-intFW0":
		if switch3:
			create_nic(server, name, network)
			create_nic(server, name, network)
			storeFW_inDB(server, name, "intFW", switch1, switch2, switch3, switch4)
		else:
			create_nic(server, name, network)
			storeFW_inDB(server, name, "intFW", switch1, switch2, switch3, switch4)

def genIP(server, vm_name, counter, vm_type, switch1, network = None, switch2 = None, switch3 = None, switch4 = None):

	if vm_type == "web" or vm_type == "mail" :
		ip = "172.17.1." + str(counter)
		storeInfo_inDB(server, vm_name, vm_type, switch1, switch2, switch3, switch4, ip, gateway = "172.17.1.1")

	if vm_type == "client" or vm_type == "vpn" :
		ip = "172.17.3." + str(counter)
		storeInfo_inDB(server, vm_name, vm_type, switch1, switch2, switch3, switch4, ip, gateway = "172.17.3.1")

	if vm_type == "log" or vm_type == "file" :
		ip = "172.17.4." + str(counter)
		storeInfo_inDB(server, vm_name, vm_type, switch1, switch2, switch3, switch4, ip, gateway = "172.17.4.1")

		get_mac_addresses(server, vm_name)
	
	if vm_type == "pFW":
		configFW_NIC(server, "a-pFW0", network, switch1, switch2, switch3, switch4)

	if vm_type == "intFW":
		configFW_NIC(server, "a-intFW0", network, switch1, switch2, switch3, switch4)
