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
		DS = DataStore()
		ctrl = controller()
		myFile = open('output.txt', 'w')
		myFile.write(str(ret))
		myFile.close()
		looptime = ret['ServerState']['ServerTiers']['DB']['ServerStartTurnTime']
		coef = (ret["ServerState"]["CostPerServer"] / ret["ServerState"]["ProfitConstant"])

		DS.setCoef(coef)

		#while ret['ServerState']['TurnNo'] < 10080:
		while True:
			x = 0

			while x <=looptime-1:
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

				DS.avgDemand(demand)
				DS.setConfig(config)

				conn.close()
				x+=1


			#Calculate free space
			capacity = [ ( ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['WEB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'] ) / 2]
			capacity.append(( ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['JAVA']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'] ) / 2)
			capacity.append(( ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][0]['UpperLimit'] + ret['ServerState']['ServerTiers']['DB']['ServerPerformance']['CapactityLevels'][1]['UpperLimit'] ) / 2)

			DS.setCapacity(capacity)
			changes = ctrl.calc(DS)
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
					}
				}
			

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
			ret = json.loads(str((response.status, response.reason, response.read())[2]))




			value = {
			"Command": "PLAY",
			"Token": "8051bf89-e115-4147-8e5a-ff9d6f39f0d7"
			#"Token": "7440b0b0-c5a2-4ab3-bdc3-8935865bb9d1",
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

			DS.resetDemand(demand)
			DS.setConfig(config)

			conn.close()
			print 'Turn: ' + str(ret['ServerState']['TurnNo'])
			print demand
			print '  ' + str(config[0]) + '    ' + str(config[1]) + '    ' + str(config[2]) + '    ' + '\n  ' + str(config[3]) + '    ' + str(config[4]) + '    ' + str(config[5]) + '   ' + '\n  ' + str(config[6]) + '    ' + str(config[7]) + '    ' + str(config[8])
			print ''
			conn.close()


if __name__ == "__main__":
	x = ServerConnector()