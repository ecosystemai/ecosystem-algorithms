from prediction.endpoints import worker_aws as endpoints
from prediction import request_utils

def set_credentials(auth, cred_string, info=False):
	ep = endpoints.SET_CREDENTIALS
	param_dict = {
		"string": cred_string
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def post_set_credentials(auth, data, info=False):
	ep = endpoints.POST_SET_CREDENTIALS
	resp = request_utils.create(auth, ep, data=data, info=info)
	result = resp.json()
	return result

def set_tenant(auth, tenant_string, info=False):
	ep = endpoints.SET_TENANT
	param_dict = {
		"string": tenant_string
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def manage_tenant(auth, tenant, action, info=False):
	ep = endpoints.MANAGE_TENANT
	param_dict = {
		"tenant": tenant,
		"action": action
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def create_tenant(auth, tenant, info=False):
	ep = endpoints.CREATE_TENANT
	param_dict = {
		"tenant": tenant,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def post_create_tenant(auth, data, info=False):
	ep = endpoints.POST_CREATE_TENANT
	resp = request_utils.create(auth, ep, data=data, info=info)
	result = resp.json()
	return result

def delete_tenant(auth, tenant, action, info=False):
	ep = endpoints.DELETE_TENANT
	param_dict = {
		"tenant": tenant,
		"action": action
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def set_configuration(auth, conf_string, info=False):
	ep = endpoints.SET_CONFIGURATION
	param_dict = {
		"string": conf_string
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def validate_tenant(auth, tenant, info=False):
	ep = endpoints.VALIDATE_TENANT
	param_dict = {
		"tenant": tenant,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def get_status(auth, tenant, info=False):
	ep = endpoints.GET_STATUS
	param_dict = {
		"tenant": tenant,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def list_tenants(auth, info=False):
	ep = endpoints.LIST_TENANTS
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result