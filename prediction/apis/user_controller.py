from prediction.endpoints import user_controller as endpoints
from prediction import request_utils

def users(auth, filterByage, filterBycity, filterByemail, filterByfirstName, filterBylastName, filterBylogin, filterBystreet, filterByzipcode, orderBy, pageNumber, pageSize, sortBy, info=False):
	ep = endpoints.USERS
	param_dict = {
		"filterByage": filterByage,
		"filterBycity": filterBycity,
		"filterByemail": filterByemail,
		"filterByfirstName": filterByfirstName,
		"filterBylastName": filterBylastName,
		"filterBylogin": filterBylogin,
		"filterBystreet": filterBystreet,
		"filterByzipcode": filterByzipcode,
		"orderBy": orderBy,
		"pageNumber": pageNumber,
		"pageSize": pageSize,
		"sortBy": sortBy
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def post_users(auth, json, info=False):
	ep = endpoints.POST_USERS
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def get_current_user(auth, info=False):
	ep = endpoints.USERS_CURRENT
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result
