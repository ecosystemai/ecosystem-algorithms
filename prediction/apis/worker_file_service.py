from prediction.endpoints import worker_file_service as endpoints
from prediction import request_utils

def upload_file(auth, path, target_path, info=False):
	"""
	Upload a file to the ecosystem-server

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param path: The path of the file to be uploaded.
	:param target_path: The path where the file will be uploaded.
	"""
	ep = endpoints.UPLOAD_FILE
	fileFp = open(path, "rb")
	files = {"file": fileFp}
	data = {"path": target_path}
	resp = request_utils.create_only_auth_no_error(auth, ep, data=data, files=files)
	return resp

def update_properties(auth, properties, info=False):
	ep = endpoints.UPDATE_PROPERTIES
	resp = request_utils.create_only_auth(auth, ep, data=properties)
	return resp

def get_file_tail(auth, path, file_path, lines, info=False):
	ep = endpoints.GET_FILE_TAIL
	param_dict = {
		"file": file_path,
		"lines": lines,
		"path": path
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	data = resp.content.decode("utf-8")[1:-1]
	rows = data.split("\n")
	new_rows = []
	new_rows.append(rows[0])
	for i in range(1, len(rows), info=False):
		row = rows[i]
		new_rows.append(row[2:])
	new_data = "\n".join(new_rows)
	return new_data

def get_file(auth, path, file_path, lines, info=False):
	ep = endpoints.GET_FILE
	param_dict = {
		"file": file_path,
		"lines": lines,
		"path": path
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	data = resp.content.decode("utf-8")[1:-1]
	rows = data.split("\n")
	new_rows = []
	new_rows.append(rows[0])
	for i in range(1, len(rows), info=False):
		row = rows[i]
		new_rows.append(row[2:])
	new_data = "\n".join(new_rows)
	return new_data

def get_property(auth, property_key, info=False):
	ep = endpoints.GET_PROPERTY
	param_dict = {
		"key": property_key
	}
	resp = request_utils.create_only_auth(auth, ep, params=param_dict, info=info)
	data = resp.content.decode("utf-8")
	return data

def get_files(auth, path="./", user="", info=False):
	ep = endpoints.GET_FILES
	param_dict = {
		"path": path,
		"user": user
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def copy_file(auth, from_path, to_path, user="", info=False):
	ep = endpoints.COPY_FILE
	param_dict = {
		"from": from_path,
		"to": to_path,
		"user": user
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	return resp

def download(auth, target_path, download_path, info=False):
	"""
	Download a file from the ecosystem-server

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param target_path: The path of the file to be downloaded.
	:param download_path: The path where the downloaded file will be saved.
	"""
	ep = endpoints.DOWNLOAD
	param_dict = {
		"name": target_path,
		"path": ""
	}
	resp = request_utils.create(auth, ep, params=param_dict, stream=True, info=info)
	with open(download_path, "wb") as fd:
		for chunk in resp.iter_content(chunk_size=128):
			fd.write(chunk)
	return resp

def delete_file(auth, path, user="", info=False):
	ep = endpoints.DELETE_FILE
	param_dict = {
		"path": path,
		"user": user
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	return resp

def file_delete(auth, path, info=False):
	ep = endpoints.FILE_DELETE
	param_dict = {
		"path": path
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	return resp

def convert_remove_non_printables(auth, infile, outfile, info=False):
	ep = endpoints.CONVERT_REMOVE_NON_PRINTABLES
	param_dict = {
		"inFile": infile,
		"outFile": outfile
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	return resp

def process_push(auth, json, info=False):
	ep = endpoints.PROCESS_PUSH
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def convert_csv_from_to(auth, char, infile, outfile, info=False):
	ep = endpoints.CONVERT_CSV_FROM_TO
	param_dict = {
		"char": char,
		"inFile": infile,
		"outFile": outfile
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	return resp

def convert_text_file_from_to(auth, in_delimiter, infile, out_delimiter, outfile, rules, info=False):
	ep = endpoints.CONVERT_TEXT_FILE_FROM_TO
	param_dict = {
		"inDelimiter": in_delimiter,
		"inFile": infile,
		"outDelimiter": out_delimiter,
		"outFile": outfile,
		"rules": rules
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	return resp