require "mcollective"
require "pp"
require "stage3/util"

include MCollective::RPC

def kickstart(opts = {})
  o = {
    :db => nil,
    :instance => nil,
    :noop => false
  }.merge(opts)
  
  db = o[:db]
  instance = o[:instance]
  hostname = instance["hostname"]
  
  collection = db.collection("interface")
  interfaces = collection.find_one(:instance => instance["id"])
  mac_pattern = build_mac_pattern(interfaces)
  
  log "Using #{mac_pattern} to filter instance"
  
  rpc_options = {
    :progress => false, 
    :verbose => true
  }

  client_ca = rpcclient("puppetca", rpc_options)
  
  client = rpcclient("provision", rpc_options)
  client.fact_filter "macaddress", mac_pattern, "=~"

  if not o[:noop]
    log "Setting hostname"
    client.set_hostname(:hostname => hostname)
    
    log "Attempting to clean existing certificate on CA (if any)"
    client_ca.clean(:certname => hostname)
    
    log "Requesting certificate"
    client.run_puppet
    
    log "Attempting to sign certificate on CA"
    client_ca.sign(:certname => hostname)
    
    log "Running Puppet"
    client.run_puppet

    printrpcstats
  end
end

def build_mac_pattern(interfaces)
  mac_addresses = Array.new
  
  interfaces.each do |i|
    mac_addresses.push(i["mac_address"])
  end
  
  return "/^(" + mac_addresses.join('|') + ")$/"
end