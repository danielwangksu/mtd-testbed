from pysphere import VIServer, VIProperty 
from pysphere.resources import VimService_services as VI 

s = VIServer() 
s.connect("192.168.1.15", "ian", "ccdc2013!")

def add_virtual_switch(network_system, name, num_ports, bridge_nic=None, mtu=None): 
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
    s._proxy.AddVirtualSwitch(request) 

def add_port_group(name, vlan_id, vswitch): 
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

    s._proxy.AddPortGroup(request) 

#Get the first host system 
host_system = s.get_hosts().keys()[0] 
print "host" + host_system
prop = VIProperty(s, host_system) 

#print existing virtual switchs 
for vs in prop.configManager.networkSystem.networkInfo.vswitch: 
    print vs.name 

#print NIC keys 
for pnic in prop.configManager.networkSystem.networkInfo.pnic: 
   print pnic.key 

#Add vswitch to the first physicall nic 
#nic = prop.configManager.networkSystem.networkInfo.pnic[0].key 

network_system = prop.configManager.networkSystem._obj 
vswitch_name = "My New VSwitch2" 
num_ports = 144 

#I'm commenting the bridge_nic parameter, because it will fail 
#if the given nic is used in another vswitch, check if it works 
#for you when providing an available physical nic 

add_virtual_switch(network_system, vswitch_name, num_ports) #, bridge_nic=nic) 

#Add a port group 
vlan_id = 1
add_port_group(network_system, vlan_id, vswitch_name) 

s.disconnect()
