import httplib, json, socket
 class ServerConnector:
 	def init(self):
		value = {
		"Command": "INIT",
		"Token": "8051bf89-e115-4147-8e5a-ff9d6f39f0d7"
			# "ChangeRequest": nil
		}
		headers = {
		            'Content-type': 'application/json',
		            'Accept': 'application/json',
		            }

		jvalue = json.dumps(value)
		conn = httplib.HTTPConnection('107.20.243.77', 80)
		conn.request('POST', '/api/hermes', jvalue, headers)
		response = conn.getresponse()
		ret = (response.status, response.reason, response.read())
		
		conn.close()