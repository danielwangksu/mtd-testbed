require "mcollective"
require "mongo"

require "stage3/util"
require "stage3/config-manifest"
require "stage3/config-network"
require "stage3/kickstart"

include Mongo

o = {
  :noop => true
}

def scan_instances(db)
  collection = db.collection("instance")
  instances = collection.find(:status => "provisioned")
  
  instances.each do |instance|
    hostname = instance["hostname"]
    
    log "Found unconfigured host #{hostname}"
    log "Generating configuration"
    
    generate_network_config :hostname => hostname, :db => db, :noop => o[:noop]
    generate_puppet_manifest :instance => instance, :noop => o[:noop]
    
    log "Attempting stage 3 of kickstart"
    
    kickstart :hostname => hostname, :db => db, :noop => o[:noop]
    
    log "Finished configuring host #{hostname}"
    
    instance["status"] = "configured"
    if not o[:noop]
      collection.update({ "_id" => instance["id"] }, instance)
      log "Saved state to the database"
    end
  end
end

## Connect to database
connection = Connection.new
db = connection.db("fixture")

## Event loop
log "Starting event loop -- press CTRL + C to stop"
while true
  log "Waiting for instances to be provisioned..."
  scan_instances(db)
  sleep 5
end