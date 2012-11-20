require "erb"
require "mcollective"
require "stage3/util"

include MCollective::RPC

## Model for the template
class Interface
	attr_accessor :name, :address, :netmask, :gateway, :dhcp
end

def generate_network_config(opts = {})
  o = {
    :db => nil,
    :instance => nil,
    :noop => false
  }.merge(opts)
  
  db = o[:db]
  instance = o[:instance]
  hostname = instance["hostname"]
  
  collection = db.collection("interface")

  ## Create an RPC client for the node
  mco = rpcclient("rpcutil")

  ## Define the host we're configuring
  mac_pattern = build_mac_pattern(collection.find(:instance => instance["_id"]))
  mco.fact_filter "macaddress", mac_pattern, "=~"

  ## Query the node for an inventory
  result = mco.inventory.first
  if result.nil?
    return false
  end

  facts = result[:data][:facts]

  ## Array of template model instances, NOT TO BE CONFUSED with database model instances
  ifaces = Array.new

  facts.each_pair do |key, value|
    if key =~ /^macaddress_(eth.*)/
      iface = Interface.new
      iface.name = $1

      # ugly ugly ugly
      interface = collection.find_one(:mac_address => value)
      if interface.nil? or interface["ip_address"].nil?
	iface.dhcp = true
      
	log "Setting interface #{iface.name} as DHCP"
      else
	iface.address = interface["ip_address"]
	iface.netmask = interface["netmask"]
	iface.gateway = interface["gateway"]
      
	log "Setting interface #{iface.name} as static with addr #{iface.address}"
      end

      ifaces.push(iface)
    end
  end
  
  out = ERB.new(File.read('templates/interfaces.erb')).result(binding)

  if o[:noop]
    puts out
  else
    directory = "/etc/puppet/files/#{hostname}/etc/network/"
    FileUtils.mkpath directory
    File.open(directory + "interfaces", "w+") do |f|
      f.write(out)
    end
  end

  return true
end
