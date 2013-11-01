import socket, sys
class ServerConnector:
	def init(self):
		self.port = raw_input("Please Enter the port being used: ")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(("hackathon.hopto.org", int(self.port)))
		self.sock.send("INIT TeamName")
		print self.sock.recv(4096)

	def send(self, toSend):
			self.sock.send(toSend)

	def recv(self):
		recv = self.sock.recv(4096)
		if recv = 'END':
			print "DONE"
		return recv
