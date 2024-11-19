from prediction.endpoints import ecosystem_home as endpoints
from prediction import request_utils

def get_v1_health(auth, info=False):
	ep = endpoints.GET_V1_HEALTH
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result

def post_v1_health(auth, notification, info=False):
	ep = endpoints.POST_V1_HEALTH
	param_dict = {"notification": notification}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def ping(auth, message, info=False):
	ep = endpoints.PING
	param_dict = {"message": message}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def fling(auth, message, info=False):
	ep = endpoints.FLING
	param_dict = {"message": message}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result