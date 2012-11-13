require "erb"
require "mcollective"
require "mongo"
require "pp"

class Interface
	attr_accessor :name, :address, :network, :gateway

	def initialize(name, address, network, gateway)
		@name = name
		@address = address
		@network = network
		@gateway = gateway
	end
end

template = %{
auto lo
iface lo inet loopback

<% for iface in interfaces %>
auto <%= iface.name %>
iface <%= iface.name %> inet static
	address <%= iface.address %>
	network <%= iface.network %>
	<% if iface.gateway %>
	gateway <%= iface.gateway %>
	<% end %>

<% end %>
}

hostname = "hornet01"

# Connect to the Mongo database
connection = Mongo::Connection.new
db = connection.db("vm_db_fixture")
instances = db.collection("instance")

# Create an RPC client for the node
mco = MCollective::RPC.rpcclient("rpcutil")
mco.fact_filter "hostname", hostname

# Query the node for an inventory
result = mco.inventory.first
facts = result[:data][:facts]

pp facts