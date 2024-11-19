from prediction.endpoints import interactions as endpoints
from prediction import request_utils

def interaction(auth, json, info=False):
	ep = endpoints.INTERACTION
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result