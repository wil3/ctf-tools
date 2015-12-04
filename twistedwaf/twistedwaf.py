""" This script provides a basic WAF based on Twisted. It allows for dynamic auto updateable rules specified in configurable python scripts.
"""
__author__ = "Wil Koch"
__contact__= "wfkoch@gmail.com"

import logging
from twisted.internet import protocol, reactor
from optparse import OptionParser 
import imp
import os.path, time

# These two classes have been adapted from http://blog.laplante.io/2013/08/a-basic-man-in-the-middle-proxy-with-twisted/
class ProxyClientInterfaceProtocol(protocol.Protocol):
	def __init__(self):
		self.logger = logging.getLogger('ClientInterface')
		self.buffer = None
		self.client = None
		self.rulelastmodified = 0

	def connectionMade(self):
		factory = protocol.ClientFactory()
		factory.protocol = ProxyServerInterfaceProtocol
		factory.server = self
		self.logger.debug("Connection from " + str(self.transport.getPeer()))

		reactor.connectTCP(self.factory.server_addr, self.factory.server_port, factory)

	# Client => Proxy
	def dataReceived(self, data):
		self.logger.debug("Data received from client:\n" + data)
		try:
			if self.client:
				self.client.write(data)
			else:
				self.buffer = data
		except Exception as e:
			self.logger.exception(e)
	
	# Proxy => Client
	def write(self, data):
		self.logger.debug("Responding back to client")
		self.transport.write(data)


class ProxyServerInterfaceProtocol(protocol.Protocol): #client to the server
	"""Interface with origin server"""

	RULE_MODULE = 'wafrule'
	def __init__(self):
		self.logger = logging.getLogger('ServerInterface')
		self.rule = None	

	def connectionMade(self):
		self.logger.debug("connection made")	
		self.factory.server.client = self
		self.peer = self.factory.server.transport.getPeer()

		port = self.factory.server.factory.port 
		#To try and limit the j
		ruleFile = self.factory.server.factory.rule
		if not self.rule or self.factory.server.rulelastmodified < os.path.getmtime(ruleFile):
			self.factory.server.rulelastmodified = os.path.getmtime(ruleFile)
			module_ = imp.load_source(self.RULE_MODULE, ruleFile)	
			self.rule = module_.WAFRule(port)

		self.write(self.factory.server.buffer)
		self.factory.server.buffer = ''

	# Server => Proxy
	def dataReceived(self, data):
		self.logger.debug("Received data from server")	
		self.factory.server.write(data)

	# Proxy => Server
	def write(self, data):
		# Before we write to our server, reload inspection code
		# to determine if we should forward the request
		if data:
			shouldBlock = False
			try:
				if self.rule:
					shouldBlock = self.rule.shouldBlock(self.peer, data)
			except Exception as e:
				self.logger.exception(e)

			if shouldBlock:
				# Abort terminates connnection immediately
				self.factory.server.transport.abortConnection()
			else:
				self.transport.write(data)



def main(port, server_addr, server_port, options):
	factory = protocol.ServerFactory()
	factory.protocol = ProxyClientInterfaceProtocol
	factory.server_addr = server_addr
	factory.server_port = server_port
	factory.rule = options.rule
	#TODO is there another way in the protocol to get port instead of this?
	factory.port = port
	reactor.listenTCP(port, factory)
	reactor.run()


if __name__ == '__main__':
	usage = "usage: %prog [options] [port] [originaddr] [originport]"
	parser = OptionParser(usage=usage)
	parser.add_option('-r', '--rule', action="store", default=None, help="Optional path to rule script.")
	parser.add_option('-v', '--verbose', action="store_true", default=False, help="Set logging to debug, output more stuff.")
	(options, args) = parser.parse_args()
	if len(args) != 3:
		parser.print_help()
		exit()

	logLevel = logging.DEBUG if options.verbose else logging.INFO	
	logging.basicConfig(level=logLevel)
	
	main(int(args[0]), args[1], int(args[2]), options)



