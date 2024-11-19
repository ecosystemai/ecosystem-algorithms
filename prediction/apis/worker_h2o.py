from prediction.endpoints import worker_h2o as endpoints
from prediction import request_utils

def train_model(auth, modelid, modeltype, params, info=False):
	ep = endpoints.BUILD_MODEL
	param_dict = {"model_id": modelid, "model_type": modeltype, "model_parms": params}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp
	# result = resp.json()
	return result

def cancel_job(auth, jobid, info=False):
	ep = endpoints.CANCEL_JOB
	param_dict = {"job_id": jobid}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def delete_frame(auth, frame, info=False):
	ep = endpoints.DELETE_FRAME
	param_dict = {"frame": frame}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	# result = json.resp()
	result = resp
	return result

def download_model_mojo(auth, modelid, info=False):
	ep = endpoints.DOWNLOAD_MODEL_MOJO
	param_dict = {"model_id": modelid}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_train_model(auth, modelid, modeltype, info=False):
	ep = None
	if modeltype == "AUTOML":
		ep = endpoints.GET_AUTO_ML_MODEL
	else:
		ep = endpoints.GET_MODEL
	param_dict = {"model_id": modelid}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	try:
		result = resp.json()
		return result
	except:
		return resp

def get_frame(auth, frameid, info=False):
	ep = endpoints.GET_FRAME
	param_dict = {"frame_id": frameid}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	try:
		result = resp.json()
		return result
	except:
		return resp

def get_frame_columns(auth, frameid, info=False):
	ep = endpoints.GET_FRAME_COLUMNS
	param_dict = {"frame_id": frameid}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_model_stats(auth, modelid, source, statstype, info=False):
	ep = endpoints.GET_MODEL_STATS
	param_dict = {"model_id": modelid, "source": source, "stats_type": statstype}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def model_grids(auth, model, info=False):
	ep = endpoints.MODEL_GRIDS
	param_dict = {"model": model}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def prediction_frames(auth, info=False):
	ep = endpoints.PREDICTION_FRAMES
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result

def prediction_jobs(auth, info=False):
	ep = endpoints.PREDICTION_JOBS
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result

def prediction_models(auth, info=False):
	ep = endpoints.PREDICTION_MODELS
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result

def file_to_frame(auth, file_name, first_row_column_names, separator, info=False):
	ep = endpoints.PROCESS_FILE_TO_FRAME_IMPORT
	param_dict = {"file_name": file_name, "first_row_column_names": first_row_column_names, "separator": separator}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def featurestore_to_frame(auth, userframe, info=False):
	ep = endpoints.PROCESS_TO_FRAME_PARSE
	resp = request_utils.create(auth, ep, json=userframe, info=info)
	parsed_frame = resp.json()
	return parsed_frame
	
def split_frame(auth, frame, ratio, info=False):
	ep = endpoints.SPLIT_FRAME
	param_dict = {"frame": frame, "ratio": ratio}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def generate_model_detail(auth, info=False):
	"""
	Process the models saved to the ecosystem-server and generate the model details for display on the ecosystem-workbench.

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	"""
	ep = endpoints.GENERATE_MODEL_DETAIL
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result

def download_model(auth, mojo_id, predict_id, info=False):
	ep = endpoints.DOWNLOAD_MODEL
	param_dict = {"mojo_id": mojo_id, "predict_id": predict_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def import_sql_table(auth, json, info=False):
	ep = endpoints.IMPORT_SQL_TABLE
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def change_to_enum(auth, frame, column, info=False):
	ep = endpoints.CHANGE_TO_ENUM
	param_dict = {"frame": frame, "column": column}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_frame_column_summary(auth, frame, column, info=False):
	ep = endpoints.GET_FRAME_COLUMN_SUMMARY
	param_dict = {"frame": frame, "column": column}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def export_frame(auth, frame, info=False):
	ep = endpoints.EXPORT_FRAME
	param_dict = {"frame": frame}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

