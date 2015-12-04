"""
	Note: WHILE THIS FILE IS OPEN IT CAN NOT BE LOADED
"""

class WAFRule:
	def __init__(self, port):
		self.port = port

	#TODO a better but more complicated method we be to return fake data
	def shouldBlock(self, peer, data):
		""" Inspect the data, determine if connection should be terminated
		Args:	
			port: Port of the server so can map to service
			peer: tuple  (protocol, client ip, client port)
			data: TCP data
		Return:
			True if should terminate connection
		"""
		return False	
