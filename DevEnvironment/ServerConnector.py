from DataStore import DataStore
from controller import controller
import httplib, json, socket


class ServerConnector:
 	def __init__(self):
		value = {
		"Command": "INIT",
		"Token": "8051bf89-e115-4147-8e5a-ff9d6f39f0d7"
		#"Token": "7440b0b0-c5a2-4ab3-bdc3-8935865bb9d1"
		}
		headers = {
		            'Content-type': 'application/json',
		            'Accept': 'application/json',
		            }

		jvalue = json.dumps(value)
		conn = httplib.HTTPConnection('107.20.243.77', 80)
		#conn = httplib.HTTPConnection('uat.hermes.wha.la', 80)
		conn.request('POST', '/api/hermes', jvalue, headers)
		response = conn.getresponse()
		ret = json.loads(str((response.status, response.reason, response.read())[2]))
		conn.close()
		DS = DataStore(ret["ServerState"]["ServerTiers"]["DB"]["ServerStartTurnTime"])
		ctrl = controller()
		myFile = open('output.txt', 'w')
		myFile.write(str(ret))
		myFile.close()
		looptime = ret['ServerState']['ServerTiers']['DB']['ServerStartTurnTime']
		coef = (ret["ServerState"]["CostPerServer"] / ret["ServerState"]["ProfitConstant"])

		WebRefresh = ret["ServerState"]["ServerTiers"]["WEB"]["ServerStartTurnTime"]
		JavaRefresh = ret["ServerState"]["ServerTiers"]["JAVA"]["ServerStartTurnTime"]
		DBRefresh = ret["ServerState"]["ServerTiers"]["DB"]["ServerStartTurnTime"]

		DS.setCoef(coef)
		infra = False
		p = None
		research = None
		didGrid = False
		progression = [None, "GRID", "GREEN", None ]


		#while ret['ServerState']['TurnNo'] < 10080:
		while True:
			x = 0

			value = {
			"Command": "PLAY",
			"Token": "8051bf89-e115-4147-8e5a-ff9d6f39f0d7"
			#"Token": "7440b0b0-c5a2-4ab3-bdc3-8935865bb9d1"
			}
			headers = {
			            'Content-type': 'application/json',
			            'Accept': 'application/json',
			            }
			jvalue = json.dumps(value)
			conn = httplib.HTTPConnection('107.20.243.77', 80)
			#conn = httplib.HTTPConnection('uat.hermes.wha.la', 80)
			conn.request('POST', '/api/hermes', jvalue, headers)
			response = conn.getresponse()
			ret = json.loads(str((response.status, response.reason, response.read())[2]))
			turnnumber = ret['ServerState']['TurnNo']
			#Get demand from server
			demand = [ret['ServerState']['ServerTiers']['DB']['ServerRegions']['NA']['NoOfTransactionsInput']]
			demand.append(ret['ServerState']['ServerTiers']['DB']['ServerRegions']['EU']['NoOfTransactionsInput'])
			demand.append(ret['ServerState']['ServerTiers']['DB']['ServerRegions']['AP']['NoOfTransactionsInput'])
			
			config = [ret['ServerState']['ServerTiers']['WEB']['ServerRegions']['NA']['NodeCount']]
			config.append(ret['ServerState']['ServerTiers']['WEB']['ServerRegions']['EU']['NodeCount'])
			config.append(ret['ServerState']['ServerTiers']['WEB']['ServerRegions']['AP']['NodeCount'])

			config.append(ret['ServerState']['ServerTiers']['JAVA']['ServerRegions']['NA']['NodeCount'])
			config.append(ret['ServerState']['ServerTiers']['JAVA']['ServerRegions']['EU']['NodeCount'])
			config.append(ret['ServerState']['ServerTiers']['JAVA']['ServerRegions']['AP']['NodeCount'])

			config.append(ret['ServerState']['ServerTiers']['DB']['ServerRegions']['NA']['NodeCount'])
			config.append(ret['ServerState']['ServerTiers']['DB']['ServerRegions']['EU']['NodeCount'])
			config.append(ret['ServerState']['ServerTiers']['DB']['ServerRegions']['AP']['NodeCount'])

			# if turnnumber % (DBRefresh*2):
			# 	DS.resetDemand(demand)
			# else:
			# 	DS.avgDemand(demand)
			DS.runningDemand(demand)
			DS.setConfig(config)
			coef = (ret["ServerState"]["CostPerServer"] / ret["ServerState"]["ProfitConstant"])
			DS.setCoef(coef)

			conn.close()

			lastProfit = ret["ServerState"]["ProfitEarned"]
			GridCost = ret["ServerState"]["ResearchUpgradeLevels"][1]["UpgradeCost"]
			GridTurns = ret["ServerState"]["ResearchUpgradeLevels"][1]["NoOfTurnsRequired"]
			GridTotalCost = GridTurns * GridCost

			if ret['ServerState']['TurnNo'] <= 9000 and ret["ServerState"]["ProfitAccumulated"] >= GridTotalCost/10 and GridCost < (lastProfit - (lastProfit/3)):
				didGrid = True
				try:
					if ret["ServerState"]["ResearchUpgradeState"]["GRID"] == -1:
						#research = "GREEN"
						pass
				except:
					research = "GRID"
				#p = research
			#Calculate free space

			#AVERAGE CAPACITY
			# capacity = [ ( ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'] ) / 2]
			# capacity.append(( ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'] ) / 2)
			# capacity.append(( ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']  ) / 2)

			#97%
			capacity = [ ( ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']+ ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] ) / 3]
			capacity.append(( ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']  + ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] ) / 3)
			capacity.append(( ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']  + ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit']) / 3)

			#93%
			# capacity = [ ( ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']+ ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'] ) / 3]
			# capacity.append(( ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']  + ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'] ) / 3)
			# capacity.append(( ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']  + ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']) / 3)

			#100% CAPACITY
			# capacity = [ ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit']]
			# capacity.append(ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'])
			# capacity.append(ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'])

			# #90% CAPACITY
			# capacity = [ ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit']]
			# capacity.append(ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'])
			# capacity.append(ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'])
			DS.setCapacity(capacity)
			webchanges = [0,0,0,0,0,0,0,0,0]
			javachanges = [0,0,0,0,0,0,0,0,0]
			dbchanges = [0,0,0,0,0,0,0,0,0]
			
			
			if turnnumber%WebRefresh == 0:
				webchanges = ctrl.calcWeb(DS,WebRefresh*2)
			if turnnumber%JavaRefresh == 0:
				javachanges = ctrl.calcJava(DS,JavaRefresh*2)
			if turnnumber%DBRefresh == 0:
				dbchanges = ctrl.calcDB(DS,DBRefresh*2)

			changes = []
			changes.append(webchanges[0])
			changes.append(webchanges[1])
			changes.append(webchanges[2])
			changes.append(javachanges[3])
			changes.append(javachanges[4])
			changes.append(javachanges[5])
			changes.append(dbchanges[6])
			changes.append(dbchanges[7])
			changes.append(dbchanges[8])

			jsonchange = {"Servers":{
				"WEB":{
					"ServerRegions":{
						"AP":{
							"NodeCount":changes[2]
							},
						"EU":{
							"NodeCount":changes[1]
							},
						"NA":{
							"NodeCount":changes[0]
							}
						}
					},

				"JAVA":{
					"ServerRegions":{
						"NA":{
							"NodeCount":changes[3]
							},
						"EU":{
							"NodeCount":changes[4]
							},
						"AP":{
							"NodeCount":changes[5]
							}
						}
					},

				"DB":{
					"ServerRegions":{
						"NA":{
							"NodeCount":changes[6]
							},
						"EU":{
							"NodeCount":changes[7]
							},
						"AP":{
							"NodeCount":changes[8]
							}
						}
					}
				
					},
					"UpgradeInfraStructure": infra,
					"UpgradeToResearch": research


				}
			if research != None:
				research = None

			value = {
			"Command": "CHNG",
			"Token": "8051bf89-e115-4147-8e5a-ff9d6f39f0d7",
			#"Token": "7440b0b0-c5a2-4ab3-bdc3-8935865bb9d1",
			"ChangeRequest": jsonchange
			}
			headers = {
			            'Content-type': 'application/json',
			            'Accept': 'application/json',
			}
			jvalue = json.dumps(value)
			conn = httplib.HTTPConnection('107.20.243.77', 80)
			#conn = httplib.HTTPConnection('uat.hermes.wha.la', 80)

			conn.request('POST', '/api/hermes', jvalue, headers)
			response = conn.getresponse()
			ret2 = json.loads(str((response.status, response.reason, response.read())[2]))
			conn.close()
			


			print 'Turn: ' + str(ret['ServerState']['TurnNo'])
			print "WEB capacity: " + str(capacity[0])
			print "JAVA capacity: " + str(capacity[1])
			print "DB capacity: " + str(capacity[2])
			
			print "ServerCost: " + str(ret["ServerState"]["CostPerServer"])
			#print didGrid
			#if didGrid:
			try:
				inf = str(ret["ServerState"]["InfraStructureUpgradeState"]["Value"])
				if inf >=0:
					#print "INFRA value: " + inf
					pass
			except:
		 		pass
			try:
				grid = str(ret["ServerState"]["ResearchUpgradeState"]["GRID"])
				if grid != "-1":
					print "---Researching: "+ "GRID" +"---\nTurns Left: " + grid
					if int(grid) <= 1441 and int(grid) >= 1430:
						#infra = True
						pass
					else:
						infra = False
				else:
					print "GRID UPGRADE COMPLETE"
			except:
				pass

			try:
				green = str(ret["ServerState"]["ResearchUpgradeState"]["GREEN"])
				if green != "-1":
					print "---Researching: "+ "GREEN" +"---\nTurns Left: " + green
				else:
					print "GREEN UPGRADE COMPLETE"
			except:
				pass
				
				
			print demand
			print '  ' + str(config[0]) + '    ' + str(config[1]) + '    ' + str(config[2]) + '    ' + '\n  ' + str(config[3]) + '    ' + str(config[4]) + '    ' + str(config[5]) + '   ' + '\n  ' + str(config[6]) + '    ' + str(config[7]) + '    ' + str(config[8])
			print ''
			conn.close()


if __name__ == "__main__":
	x = ServerConnector()