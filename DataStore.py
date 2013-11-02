class DataStore:
	def __init__(self):
		self.demand = [0,0,0]
		self.config = [0,0,0,0,0,0,0,0,0]
		self.capacity = []

	def avgDemand(self, demand):
		#take in "demand" data and store it into the list self.demand (average it)
		self.demand[0] = (self.demand[0] + demand[0]) / 2
		self.demand[1] = (self.demand[1] + demand[1]) / 2
		self.demand[2] = (self.demand[2] + demand[2]) / 2

	def resetDemand(self, demand):
		#take in "demand" data and store it into the list self.demand
		#this time overwrite the data to start a new cycle
		self.demand[0] = demand[0]
		self.demand[1] = demand[1]
		self.demand[2] = demand[2]

	def setConfig(self, iconfig):
		#take in "iconfig" data and store it into the list self.config
		self.config = iconfig
	def setCapacity(self, icapacity):
		self.capacity = icapacity

	def getConfig(self):
		return self.config
	def getDemand(self):
		return self.demand
	def getCapacity(self):
		return self.capacity