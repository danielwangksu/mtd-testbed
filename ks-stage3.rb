require "rubygems"
require "colorize"
require "mcollective"
require "mongo"

require "stage3/util"
require "stage3/config-manifest"
require "stage3/config-network"
require "stage3/kickstart"

include Mongo

def scan_instances(db)
  noop = false
  
  collection = db.collection("instance")
  instances = collection.find(:status => "provisioned")
  
  instances.each do |instance|
    hostname = instance["hostname"]
    
    log "Found unconfigured host #{hostname}".on_blue
    log "Generating configuration"
    
    if not generate_network_config :instance => instance, :db => db, :noop => noop
      log "Could not connect to instance via MCollective; will retry next round".on_red
      next
    end

    generate_puppet_manifest :instance => instance, :noop => noop
    
    log "Attempting stage 3 of kickstart"
    
    kickstart :instance => instance, :db => db, :noop => noop
    
    log "Finished configuring host #{hostname}".black.on_green
    
    instance["status"] = "configured"
    if not noop
      collection.update({ "_id" => instance["_id"] }, instance)
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
  sleep 30
end
