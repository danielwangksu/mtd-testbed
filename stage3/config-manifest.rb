require "erb"
require "pp"
require "stage3/util"

class Instance
  attr_accessor :hostname, :tag

  def initialize(hostname, tag)
    self.hostname = hostname
    self.tag = tag
  end
end

def generate_puppet_manifest(opts = {})
  o = {
    :instance => nil,
    :noop => false
  }.merge(opts)
  
  instance = Instance.new(o[:instance]["hostname"], o[:instance]["tag"])

  out = ERB.new(File.read('templates/manifest.erb')).result(binding)

  if not o[:noop]
    directory = "/etc/puppet/manifests/nodes/"
    FileUtils.mkpath directory
    File.open(directory + hostname + ".pp", "w+") do |f|
      f.write(out)
    end
  end
end