from runtime.apis import runtime_engine

class Authenticate:
	"""
	Logs into the ecosystem runtime and retrieves an access token for authentication.

	:param api_address: The url of the ecosystem runtime.
	"""
	def __init__(self, api_address):
		self.api_address = api_address
		self.auth_headers = {
			"Accept": "*/*"
		}
		message = "Login Successful"
		output = runtime_engine.no_auth_ping(api_address, "/ping", self.auth_headers, message)
		print(output)
		if output["message"] != "":
			print("Login Successful")
		else:
			print("Login Not Successful")

	def get_server(self):
		return self.api_address

	def get_auth_headers(self):
		return self.auth_headers