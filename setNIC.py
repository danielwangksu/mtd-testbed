from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

# connect to server
server = VIServer()
server.connect("192.168.1.15", "ian", "ccdc2013!")
print server.get_server_type()

vm = "BT5R2"
vm_obj=server.get_vm_by_name(vm) 
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
    net_device.Backing.set_element_deviceName("N127 Physical Network")
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
        print "VM %s successfully reconfigured" % vm 
    elif status == task.STATE_ERROR: 
        print "Error reconfiguring vm: %s" % vm,task.get_error_message() 
    else: 
    	print "Vm %s not found" % vm
