from prediction.endpoints import auth_controller as endpoints
from prediction import request_utils

# AUTH_LOGIN See jwt_access

def refresh_token(auth, refresh_token, info=False):
	ep = endpoints.AUTH_REFRESH_TOKEN
	resp = request_utils.create(auth, ep, json=refresh_token, info=info)
	meta = resp.json()
	return meta

def request_password(auth, json, info=False):
	ep = endpoints.AUTH_REQUEST_PASS
	resp = request_utils.create(auth, ep, json=json, info=info)
	meta = resp.json()
	return meta

def reset_password(auth, json, info=False):
	ep = endpoints.AUTH_RESET_PASS
	resp = request_utils.create(auth, ep, json=json, info=info)
	meta = resp.json()
	return meta

def restore_password(auth, json, info=False):
	ep = endpoints.AUTH_RESTORE_PASS
	resp = request_utils.create(auth, ep, json=json, info=info)
	meta = resp.json()
	return meta

def sign_out(auth, info=False):
	ep = endpoints.AUTH_SIGN_OUT
	resp = request_utils.create(auth, ep, info=info)
	meta = resp.json()
	return meta

def sign_out(auth, info=False):
	ep = endpoints.AUTH_SIGN_OUT
	resp = request_utils.create(auth, ep, info=info)
	meta = resp.json()
	return meta

def sign_up(auth, json, info=False):
	ep = endpoints.AUTH_SIGN_UP
	resp = request_utils.create(auth, ep, info=info)
	meta = resp.json()
	return meta