from prediction.endpoints import ecosystem_user_profiles as endpoints
from prediction import request_utils

def validate(auth, userid, password, info=False):
	ep = endpoints.VALIDATE
	param_dict = {
		"userid": userid,
		"password": password
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def profile(auth, userid, info=False):
	ep = endpoints.PROFILE
	param_dict = {
		"userid": userid
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def archive(auth, userid, info=False):
	ep = endpoints.ARCHIVE
	param_dict = {
		"userid": userid
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def activities(auth, user, info=False):
	ep = endpoints.ACTIVITIES
	param_dict = {
		"user": user
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def post_activity(auth, json, info=False):
	ep = endpoints.POST_ACTIVITY
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result