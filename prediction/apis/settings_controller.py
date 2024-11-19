from prediction.endpoints import settings_controller as endpoints
from prediction import request_utils

def current(auth, info=False):
	ep = endpoints.CURRENT
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result
