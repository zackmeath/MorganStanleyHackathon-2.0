from DataStore import DataStore
class controller:
	def __init__(self):
		self.changeNums = [0,0,0,0,0,0,0,0,0]

	def calcDB(self,ds):
		self.changeNums = [0,0,0,0,0,0,0,0,0]
		cap = ds.getCapacity()
		config = ds.getConfig()
		current = [
		config[0] * cap[0],
		config[1] * cap[0],
		config[2] * cap[0],
		config[3] * cap[1],
		config[4] * cap[1],
		config[5] * cap[1],
		config[6] * cap[2],
		config[7] * cap[2],
		config[8] * cap[2]
		]


		demand = ds.getDemand()
		coef = ds.getCoef()
		jcoef = (cap[1]*coef)/cap[0]
		dcoef = (cap[2]*jcoef)/cap[1]
		#figure out database changes
		#only use EU DB
		databaseDemand = demand[0] + demand[1] + demand[2]
		databaseCurrent = config[7] * cap[2]
		if databaseDemand < 25:
			return [
			-1*config[0],
			-1*config[1],
			-1*config[2],
			-1*config[3],
			-1*config[4],
			-1*config[5],
			-1*config[6],
			-1*config[7],
			-1*config[8]
			]

		if databaseDemand - dcoef > databaseCurrent:
			while databaseDemand - dcoef > databaseCurrent:
				self.changeNums[7]+=1
				databaseCurrent+=cap[2]
		elif databaseCurrent > databaseDemand + (cap [2] + dcoef):
			while databaseCurrent > databaseDemand + (cap [2] + dcoef):
				#print "while " + str(databaseCurrent) + ' > ' + str(databaseDemand) + " + " + str((cap [2] - (cap[2]/5)))
				self.changeNums[7]-=1
				databaseCurrent-=cap[2]
		return self.changeNums



	def calcWeb(self,ds):
		#return list of changes
		self.changeNums = [0,0,0,0,0,0,0,0,0]
		cap = ds.getCapacity()
		config = ds.getConfig()
		current = [
		config[0] * cap[0],
		config[1] * cap[0],
		config[2] * cap[0],
		config[3] * cap[1],
		config[4] * cap[1],
		config[5] * cap[1],
		config[6] * cap[2],
		config[7] * cap[2],
		config[8] * cap[2]
		]


		demand = ds.getDemand()
		coef = ds.getCoef()
		if demand[0] + demand[1] + demand[2] < 25:
			return [
			-1*config[0],
			-1*config[1],
			-1*config[2],
			-1*config[3],
			-1*config[4],
			-1*config[5],
			-1*config[6],
			-1*config[7],
			-1*config[8]
			]
		#WEB tier
		#0
		if demand[0] - coef  > current[0]: 
			while demand[0] - coef > current[0]:
				self.changeNums[0]+=1
				current[0]+=cap[0]

		elif current[0] > demand[0] + (cap [0] + coef):
			while current[0] > demand[0] + (cap [0] + coef):
				self.changeNums[0]-=1
				current[0]-=cap[0]

		#1
		if demand[1] - coef > current[1]: 
			while demand[1] - coef > current[1]:
				self.changeNums[1]+=1
				current[1]+=cap[0]

		elif current[1] > demand[1] + (cap [0] + coef):
			while current[1] > demand[1] + (cap [0] + coef):
				self.changeNums[1]-=1
				current[1]-=cap[0]

		#2
		if demand[2] - coef > current[2]: 
			while demand[2] - coef > current[2]:
				self.changeNums[2]+=1
				current[2]+=cap[0]

		elif current[2] > demand[2] + (cap [0] + coef):
			while current[2] > demand[2] + (cap [0] + coef):
				self.changeNums[2]-=1
				current[2]-=cap[0]
		return self.changeNums


	def calcJava(self,ds):
		#return list of changes
		self.changeNums = [0,0,0,0,0,0,0,0,0]
		cap = ds.getCapacity()
		config = ds.getConfig()
		current = [
		config[0] * cap[0],
		config[1] * cap[0],
		config[2] * cap[0],
		config[3] * cap[1],
		config[4] * cap[1],
		config[5] * cap[1],
		config[6] * cap[2],
		config[7] * cap[2],
		config[8] * cap[2]
		]

		demand = ds.getDemand()
		coef = ds.getCoef()
		jcoef = (cap[1]*coef)/cap[0]
		if demand[0] + demand[1] + demand[2] < 25:
			return [
			-1*config[0],
			-1*config[1],
			-1*config[2],
			-1*config[3],
			-1*config[4],
			-1*config[5],
			-1*config[6],
			-1*config[7],
			-1*config[8]
			]
		#JAVA tier
		#3
		if demand[0] - jcoef > current[3]: 
			while demand[0] - jcoef > current[3]:
				self.changeNums[3]+=1
				current[3]+=cap[1]

		elif current[3] > demand[0] + (cap [1] + jcoef):
			while current[3] > demand[0] + (cap[1] + jcoef):
				self.changeNums[3]-=1
				current[3]-=cap[1]

		#4
		if demand[1] - jcoef > current[4]: 
			while demand[1] - jcoef > current[4]:
				self.changeNums[4]+=1
				current[4]+=cap[1]

		elif current[4] > demand[1] + (cap [1] + jcoef):
			while current[4] > demand[1] + (cap[1] + jcoef):
				self.changeNums[4]-=1
				current[4]-=cap[1]

		#5
		if demand[2] - jcoef > current[5]: 
			while demand[2] - jcoef > current[5]:
				self.changeNums[5]+=1
				current[5]+=cap[1]

		elif current[5] > demand[2] + (cap [1] + jcoef):
			while current[5] > demand[2] + (cap[1] + jcoef):
				self.changeNums[5]-=1
				current[5]-=cap[1]

		return self.changeNums