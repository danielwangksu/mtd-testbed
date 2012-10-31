from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

import config

# connect to server
server = VIServer()
server.connect("192.168.1.15", "ian", "ccdc2013!")
print server.get_server_type()
