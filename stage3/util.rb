def log(message)
  time = Time.new.ctime
  puts "[#{time}] #{message}\n"
end

def build_mac_pattern(interfaces)
  mac_addresses = Array.new
  
  interfaces.each do |i|
    mac_addresses.push(i["mac_address"])
  end
  
  pattern = "/^(" + mac_addresses.join('|') + ")$/"

  log "Using #{pattern} for fact filter"

  return pattern
end
