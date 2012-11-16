import time
from pysphere import *
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask 

from model import *
from util import *
from util_db import *

# connect to DB
connect("vm_db")

for instance in Instance.objects:
	print instance.hostname + " - " + instance.status

for instance in Instance.objects:
	instance.status = "configured"
	instance.save()

for instance in Instance.objects:
	print instance.hostname + " - " + instance.status
