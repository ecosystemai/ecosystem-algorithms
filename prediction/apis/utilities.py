from prediction.endpoints import utilities as endpoints
from prediction import request_utils

def convert_json_to_yaml(auth, json, info=False):
	ep = endpoints.CONVERT_JSON_TO_YAML
	resp = request_utils.create(auth, ep, json=json, info=info)
	yaml = resp.json()
	return yaml

def convert_range_from_to(auth, rules, value, info=False):
	ep = endpoints.CONVERT_RANGE_FROM_TO
	param_dict = {
		"rules": rules,
		"value": value
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def convert_text_file_from_to(auth, in_delimiter, in_file, out_delimiter, out_file, rules, info=False):
	ep = endpoints.CONVERT_TEXT_FILE_FROM_TO
	param_dict = {
		"inDelimiter": in_delimiter,
		"inFile": in_file,
		"outDelimiter": out_delimiter,
		"outFile": out_file,
		"rules": rules
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def convert_json_to_yaml(auth, yaml, info=False):
	ep = endpoints.CONVERT_YAML_TO_JSON
	resp = request_utils.create(auth, ep, json=yaml, info=info)
	json = resp.json()
	return json

def copy_file(auth, f_from, f_to, info=False):
	ep = endpoints.COPY_FILE
	param_dict = {
		"from": f_from,
		"to": f_to
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp
	return result

def get_file(auth, file_name, lines, info=False):
	ep = endpoints.GET_FILE
	param_dict = {
		"file": file_name,
		"lines": lines
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def execute_generic(auth, script, info=False):
	ep = endpoints.EXECUTE_GENERIC
	resp = request_utils.create(auth, ep, data=script, info=info)
	result = resp.json()
	return result

def get_config(auth, info=False):
	ep = endpoints.GET_CONFIG
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result

def create_json_from_text(auth, in_file, out_file, info=False):
	ep = endpoints.CREATE_JSON_FROM_TEXT
	param_dict = {
		"inFile": in_file,
		"outFile": out_file,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_container_log(auth, lines, type, info=False):
	ep = endpoints.GET_CONTAINER_LOGS
	param_dict = {
		"lines": lines,
		"type": type,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_rest_generic(auth, data, info=False):
	ep = endpoints.GET_REST_GENERIC
	resp = request_utils.create(auth, ep, data=data, info=info)
	result = resp.json()
	return result