require "erb"
require "mcollective"
require "mongo"
require "pp"

if ARGV.length < 1:
	puts "Usage: ruby gen-ifaces.rb <hostname>"
	exit
end

hostname = ARGV.fetch(0)

## Model for the template
class Interface
	attr_accessor :name, :address, :netmask, :gateway, :dhcp
end

## ERB template for /etc/network/interfaces
## Full of hax
template = %{
auto lo
iface lo inet loopback

<% for iface in ifaces %>
auto <%= iface.name %>
<% if iface.dhcp %>
iface <%= iface.name %> inet dhcp
<% else %>
iface <%= iface.name %> inet static
	address <%= iface.address %>
	netmask <%= iface.netmask %>
	<% if iface.gateway %>
	gateway <%= iface.gateway %>
	<% end %>
<% end %>
<% end %>
}

##
include MCollective::RPC
include Mongo

## Connect to the Mongo database
connection = Connection.new
db = connection.db("vm_db_fixture")
interfaces = db.collection("interface")

## Create an RPC client for the node
mco = rpcclient("rpcutil")

## Define the host we're configuring
mco.fact_filter "hostname", hostname

## Query the node for an inventory
result = mco.inventory.first
facts = result[:data][:facts]

## Array of template model instances, NOT TO BE CONFUSED with database model instances
ifaces = Array.new

facts.each_pair do |key, value|
	if key =~ /^macaddress_(eth.*)/
		iface = Interface.new
		iface.name = $1

		# ugly ugly ugly
		interface = interfaces.find_one(:mac_address => value)
		if interface.nil? or interface["ip_address"].nil?
			iface.dhcp = true
		else
			iface.address = interface["ip_address"]
			iface.netmask = interface["netmask"]
			iface.gateway = interface["gateway"]
		end

		ifaces.push(iface)
	end
end

out = ERB.new(template).result(binding)

File.open("output/#{hostname}-interfaces", "w+") do |f|
	f.write(out)
end
