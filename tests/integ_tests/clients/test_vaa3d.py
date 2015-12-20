
def test_try_finally():
	try:
		raise Exception("hey there mister")
	finally:
		print "DO this regardless of exception"