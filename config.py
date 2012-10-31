from pysphere import *
from pysphere.resources import VimService_services as VI

def add_new_NIC(server, vm_name, network_name):
	"""Adds a new NIC to an existing VM

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string
	@network_name: netork name string"""

	vm_obj = server.get_vm_by_name(vm_name)
	if not vm_obj:
	    raise Exception("VM %s not found" % vm_name)

	#Invoke ReconfigVM_Task
	request = VI.ReconfigVM_TaskRequestMsg()
	_this = request.new__this(vm_obj._mor)
	_this.set_attribute_type(vm_obj._mor.get_attribute_type())
	request.set_element__this(_this)
	spec = request.new_spec()
	#add a NIC. the network Name must be set as the device name.
	dev_change = spec.new_deviceChange()
	dev_change.set_element_operation("add")
	nic_ctlr = VI.ns0.VirtualPCNet32_Def("nic_ctlr").pyclass()
	nic_backing = VI.ns0.VirtualEthernetCardNetworkBackingInfo_Def("nic_backing").pyclass()
	nic_backing.set_element_deviceName(network_name)
	nic_ctlr.set_element_addressType("generated")
	nic_ctlr.set_element_backing(nic_backing)
	nic_ctlr.set_element_key(4)
	dev_change.set_element_device(nic_ctlr)

	spec.set_element_deviceChange([dev_change])
	request.set_element_spec(spec)
	ret = server._proxy.ReconfigVM_Task(request)._returnval

	#Wait for the task to finish
	task = VITask(ret, server)
	status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
	if status == task.STATE_SUCCESS:
	    print "VM %s successfully reconfigured" % vm_name

	elif status == task.STATE_ERROR:
	    print "Error reconfiguring vm: %s" % vm_name, task.get_error_message()

def reconfigure_NIC(server, vm, network_name):
	vm_name = "BT5R2"
	vm_obj=server.get_vm_by_name(vm_name) 
	if vm_obj: 
	    #Find Virtual Nic device 
	    net_device = None 
	    for dev in vm_obj.properties.config.hardware.device: 
		if dev._type in ["VirtualE1000", "VirtualE1000e", 
		                 "VirtualPCNet32", "VirtualVmxnet"]: 
		    net_device = dev._obj 
		    break 

	    if not net_device: 
		raise Exception("The vm seems to lack a Virtual Nic") 
	    #Set Nic macAddress to Manual and set address 
	    #net_device.set_element_addressType("Manual") 
	    net_device.Backing.set_element_deviceName(network_name)
	    #Invoke ReconfigVM_Task 
	    request = VI.ReconfigVM_TaskRequestMsg() 
	    _this = request.new__this(vm_obj._mor) 
	    _this.set_attribute_type(vm_obj._mor.get_attribute_type()) 
	    request.set_element__this(_this) 
	    spec = request.new_spec() 
	    dev_change = spec.new_deviceChange() 
	    dev_change.set_element_device(net_device) 
	    dev_change.set_element_operation("edit") 
	    spec.set_element_deviceChange([dev_change]) 
	    request.set_element_spec(spec) 
	    ret = server._proxy.ReconfigVM_Task(request)._returnval 

	    #Wait for the task to finish 
	    task = VITask(ret, server) 

	    status = task.wait_for_state([task.STATE_SUCCESS,task.STATE_ERROR]) 
	    if status == task.STATE_SUCCESS: 
		print "VM %s successfully reconfigured" % vm_name 
	    elif status == task.STATE_ERROR: 
		print "Error reconfiguring vm_name: %s" % vm_name,task.get_error_message() 
	    else: 
	    	print "Vm %s not found" % vm_name

def delete_vm(server, vm_name):
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
	task = VITask(ret, server)

	status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
	if status == task.STATE_SUCCESS:
	    print "VM successfully deleted from disk"
	elif status == task.STATE_ERROR:
	    print "Error removing vm:", task.get_error_message() 

def getMAC(server, vm_name):
	"""Get MAC address of a VM

	@server: server object 
		e.g. server = VIServer() 
		     server.connect("X.X.X.X", "user", "password")
	@vm_name: vm name string
	"""

	vm = server.get_vm_by_name(vm_name)

	for id, device in vm.get_property("devices").items():
		if device.has_key("macAddress"):
			print device["label"] + " - " +device["macAddress"] 

def add_virtual_switch(server, network_system, name, num_ports, bridge_nic=None, mtu=None):
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

def createSwitch(vswitch_name, port_group_name, num_ports, server, esxi_host): 
	prop = VIProperty(server, esxi_host)
	network_system = prop.configManager.networkSystem._obj 
	
	# Create vSwitch
	add_virtual_switch(server, network_system, vswitch_name, num_ports) 

	# Add a port group 
	vlan_id = 0 
	add_port_group(server, network_system, vswitch_name, vlan_id, vswitch_name) 

	return True
