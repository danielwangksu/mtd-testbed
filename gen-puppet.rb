require "erb"
require "mcollective"
require "mongo"
require "pp"

if ARGV.length < 1:
	puts "Usage: ruby gen-puppet.rb <hostname>"
	exit
end

hostname = ARGV.fetch(0)

## Model for the template
class Instance
	attr_accessor :name, :tag
end

## ERB template for HOSTNAME.pp
## Full of hax
template = %{
node "<%= instance.name %>" {
	include debian
	include <%= instance.tag %>
	
	file { "/etc/network/interfaces":
		source => "puppet:///files/<%= instance.name %>/etc/network/interfaces",
		mode => 0644,
		owner => root,
		group => root
	}
}
}

##
include MCollective::RPC
include Mongo

## Connect to the Mongo database
connection = Connection.new
db = connection.db("vm_db_fixture")
instances = db.collection("instance")

## TODO Transform hostname -> Instance model

out = ERB.new(template).result(binding)

File.open("/etc/puppet/manifests/nodes/" + hostname + ".pp", "w+") do |f|
	f.write(out)
end
