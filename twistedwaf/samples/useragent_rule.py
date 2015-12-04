"""
	Note: WHILE THIS FILE IS OPEN IT CAN NOT BE LOADED
"""
import re
class WAFRule:
	def __init__(self, port):
		self.port = port
		self.pattern = re.compile("User-Agent: curl", re.IGNORECASE)

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
		block = True if self.pattern.search(data) else False
		return block 


if __name__ == "__main__":
	curl = """
		GET / HTTP/1.1
		User-Agent: curl/7.35.0
		Host: 192.168.1.102:8000
		Accept: */*
		"""
	rule = WAFRule(666)
	print rule.shouldBlock('127.0.0.1', curl)
