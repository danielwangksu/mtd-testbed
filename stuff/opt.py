def test (a, b = None):
	if a and b:
		print "exista"
		myt(b)
	else:
		print "nu exista"
		myt(b)

def myt(b = None):
	if b:
		print b

test("a", "b")


vm_type = "web"
if vm_type != "pFW" or vm_type != "intFW":
	print "nu e egal"
