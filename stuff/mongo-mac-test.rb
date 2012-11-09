require "mongo"
require "pp"

connection = Mongo::Connection.new("localhost", 27017)
db = connection.db("puppet")

instances = db.collection("instances")

instance = instances.find(:mac => "00:00:00:00:00:00")

p instance["hostname"]