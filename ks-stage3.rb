require "mcollective"
require "mongo"
require "pp"

connection = Mongo::Connection.new("localhost", 27017)
db = connection.db("vm_db_fixture")

interfaces = db.collection("interface")

include MCollective::RPC

client_ca = rpcclient("puppetca")
client_ca.verbose = true

client_util = rpcclient("rpcutil")
client_util.progress = false

client = rpcclient("provision")
client.verbose = true

client.discover.map do |node|
    client_util.identity_filter node

    result = client_util.inventory.first
    facts = result[:data][:facts]

    macaddr = facts["macaddress"]

    interface = interfaces.find_one(:mac_address => macaddr)
    if interface.nil?
        puts "No match in database for MAC address #{macaddr}"
        next
    end
    instance = db.dereference(interface["instance"])
    hostname = instance["hostname"]

    client.fact_filter "macaddress", macaddr

    puts "Setting hostname\n"
    printrpc client.set_hostname(:hostname => hostname)
    printrpc client_ca.clean(:certname => hostname)
    puts "Requesting certificate\n"
    printrpc client.run_puppet
    printrpc client_ca.sign(:certname => hostname)
    puts "Starting Puppet run\n"
    printrpc client.run_puppet

end

printrpcstats