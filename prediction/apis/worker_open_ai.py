from prediction.endpoints import worker_open_ai as endpoints
from prediction import request_utils

def get_open_ai_result(auth, json, info=False):
	ep = endpoints.GET_OPEN_AI_RESULT
	resp = request_utils.create(auth, ep, data=json, info=info)
	parsed_frame = resp.json()
	return parsed_frame