class DataStore:
	def __init__(self, numOfValues):
		self.demand = [0,0,0]
		self.config = [0,0,0,0,0,0,0,0,0]
		self.capacity = [0,0,0]
		self.demandUS = []
		self.demandEU = []
		self.demandAP = []
		self.valuesToStore = numOfValues

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

	def runningDemand(self,demand):
		if len(self.demandUS) < self.valuesToStore:
			self.demandUS.append(demand[0])
			self.demandEU.append(demand[1])
			self.demandAP.append(demand[2])
		else:
			i = 0
			while i < self.valuesToStore-1:
				self.demandUS[i] = self.demandUS[i+1]
				i+=1
			self.demandUS[i] = demand[0]
			i = 0
			while i < self.valuesToStore-1:
				self.demandEU[i] = self.demandEU[i+1]
				i+=1
			self.demandEU[i] = demand[1]
			i = 0
			while i < self.valuesToStore-1:
				self.demandAP[i] = self.demandAP[i+1]
				i+=1
			self.demandAP[i] = demand[2]
	def setConfig(self, iconfig):
		#take in "iconfig" data and store it into the list self.config
		self.config = iconfig
	def setCapacity(self, icapacity):
		self.capacity = icapacity
	def setCoef(self, icoef):
		self.coef = icoef


	def getCoef(self):
		return self.coef 
	def getConfig(self):
		return self.config
	def getDemand(self):
		return self.demand
	def getCapacity(self):
		return self.capacity
	def getRunningDemand(self, num):
		us = 0
		i = 0
		while i < num:
			us+=self.demandUS[len(self.demandUS)-i]
			i+=1
		us = us/i

		eu = 0
		i = 0
		while i < num:
			eu+=self.demandEU[len(self.demandEU)-i]
			i+=1
		eu = eu/i

		ap = 0
		i = 0
		while i < num:
			ap+=self.demandAP[len(self.demandAP)-i]
			i+=1
		ap = ap/i

		# eu = 0
		# for data in self.demandEU:
		# 	eu+=data
		# eu = eu/len(self.demandEU)

		# ap = 0
		# for data in self.demandAP:
		# 	ap+=data
		# ap = ap/len(self.demandAP)

		return [us,eu,ap]