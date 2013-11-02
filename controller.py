from DataStore import DataStore
class controller:
	def __init__(self):
		self.changeNums = [0,0,0,0,0,0,0,0,0]
	def calc(self,ds):
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
		print ''
		print "DatabaseDemand: " + str(databaseDemand)
		print "DatabaseCurrent: " + str(databaseCurrent)
		

		if databaseDemand - (cap[2]/5) > databaseCurrent:
			while databaseDemand - (cap[2]/5) > databaseCurrent:
				self.changeNums[7]+=1
				databaseCurrent+=cap[2]
		elif databaseCurrent > databaseDemand + (cap [2] - (cap[2]/5)):
			while databaseCurrent > databaseDemand + (cap [2] - (cap[2]/5)):
				#print "while " + str(databaseCurrent) + ' > ' + str(databaseDemand) + " + " + str((cap [2] - (cap[2]/5)))
				self.changeNums[7]-=1
				databaseCurrent-=cap[2]
		print self.changeNums[7]
		
		freespace = [
		current[0] - demand[0],
		current[1] - demand[0],
		current[2] - demand[0],
		current[3] - demand[1],
		current[4] - demand[1],
		current[5] - demand[1],
		current[6] - demand[2],
		current[7] - demand[2],
		current[8] - demand[2]
		]

		x = 0
		while x <10:
			x+=1
		return self.changeNums