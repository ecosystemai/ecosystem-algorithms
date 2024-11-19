from prediction.endpoints import ecosystem_generation_engine as endpoints
from prediction import request_utils

def generate_build(auth, json, info=False):
	ep = endpoints.GENERATE_BUILD
	resp = request_utils.create(auth, ep, json=json, info=False)
	result = resp.json()
	return result

# def generate_properties(auth, json, info=False):
# 	ep = endpoints.GENERATE_PROPERTIES
# 	resp = request_utils.create(auth, ep, json=json, info=False)
# 	result = resp.json()
# 	return result

def get_build(auth, uuid, info=False):
	ep = endpoints.GET_BUILD
	param_dict = {
		"uuid": uuid
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=False)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def process_build(auth, json, info=False):
	ep = endpoints.PROCESS_BUILD
	resp = request_utils.create(auth, ep, json=json, info=False)
	result = resp.json()
	return result

def process_push(auth, json, info=False):
	"""
	Push a deployment to the ecosystem-runtime

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param json: The deployment config to be pushed to the ecosystem-runtime.
	"""
	ep = endpoints.PROCESS_PUSH
	resp = request_utils.create(auth, ep, json=json, info=False)
	result = resp.json()
	return result