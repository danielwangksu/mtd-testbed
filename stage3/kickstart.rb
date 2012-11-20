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
  interfaces = collection.find(:instance => instance["_id"])
  mac_pattern = build_mac_pattern(interfaces)
  
  rpc_options = {
    :progress => false, 
    :verbose => false
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
