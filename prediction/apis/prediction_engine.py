from prediction.endpoints import prediction_engine as endpoints
from prediction import request_utils
import json

def delete_analysis(auth, analysis_id, info=False):
	ep = endpoints.DELETE_ANALYSIS
	resp = request_utils.create(auth, ep, ep_arg=analysis_id, info=info)
	result = resp.json()
	return result

def delete_model(auth, model_id, info=False):
	ep = endpoints.DELETE_MODEL
	resp = request_utils.create(auth, ep, ep_arg=model_id, info=info)
	result = resp.json()
	return result

def delete_prediction(auth, prediction_id, info=False):
	ep = endpoints.DELETE_PREDICTION
	resp = request_utils.create(auth, ep, ep_arg=prediction_id, info=info)
	result = resp.json()
	return result

def delete_prediction_project(auth, prediction_project_id, info=False):
	ep = endpoints.DELETE_PREDICTION_PROJECT
	resp = request_utils.create(auth, ep, ep_arg=prediction_project_id, info=info)
	result = resp.json()
	return result

def delete_user_deployments(auth, user_deployments_id, info=False):
	ep = endpoints.DELETE_USER_DEPLOYMENTS
	resp = request_utils.create(auth, ep, ep_arg=user_deployments_id, info=info)
	result = resp.json()
	return result

def delete_userframe(auth, frame_id, info=False):
	ep = endpoints.DELETE_USER_FRAME
	param_dict = {"frame_id": frame_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def deploy_predictor(auth, json, info=False):
	ep = endpoints.DEPLOY_PREDICTOR
	resp = request_utils.create(auth, ep, json=json, info=info)
	response = resp.json()
	return response

def download_project(auth, project_id, module_name, info=False):
	"""
	Create a module zip file from the project specified by project_id.

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param project_id: The name of the project to be converted to a module.
	:param module_name: The name of the module specified in the project config.
	"""
	ep = endpoints.DOWNLOAD_PROJECT_ZIP
	param_dict = {"projectID": project_id, "moduleName": module_name}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	response = resp
	return response

def get_analysis_result(auth, analysis_id, info=False):
	ep = endpoints.GET_ANALYSIS_RESULT
	param_dict = {"analysis_id": analysis_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_analysis_results(auth, info=False):
	ep = endpoints.GET_ANALYSIS_RESULTS
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	results = resp.json()
	if "item" in results:
		results = results["item"]
	return results

def get_prediction(auth, predict_id, info=False):
	ep = endpoints.GET_PREDICTION
	param_dict = {"predict_id": predict_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_prediction_project(auth, project_id, info=False):
	ep = endpoints.GET_PREDICTION_PROJECT
	param_dict = {"project_id": project_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

# TODO: all these ep.get_username() call might need to be replaced with arguments that check if a  value is passed first
def get_prediction_projects(auth, info=False):
	ep = endpoints.GET_PREDICTION_PROJECTS
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	projects = resp.json()
	if "item" in projects:
		projects = projects["item"]
	return projects

def get_user_deployment(auth, user_deployments, info=False):
	ep = endpoints.GET_USER_DEPLOYMENT
	param_dict = {"user_deployments": user_deployments}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_user_deployments(auth, info=False):
	ep = endpoints.GET_USER_DEPLOYMENTS
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	deployments = resp.json()
	if "item" in deployments:
		deployments = deployments["item"]
	return deployments

def get_user_featurestores(auth, info=False):
	ep = endpoints.GET_USER_FEATURE_STORES
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	featurestores = resp.json()
	if "item" in featurestores:
		featurestores = featurestores["item"]
	return featurestores

def get_user_files(auth, info=False):
	ep = endpoints.GET_USER_FILES
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	files = resp.json()
	if "item" in files:
		files = files["item"]
	return files

def get_featurestores(auth, info=False):
	ep = endpoints.GET_USER_FRAMES
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	frames = resp.json()
	if "item" in frames:
		frames = frames["item"]
	return frames

def get_featurestore(auth, frame_id, info=False):
	ep = endpoints.GET_USER_FRAME
	param_dict = {"frame_id": frame_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	userframe = resp.json()
	return userframe

def get_uframe(auth, frame_id, info=False):
	ep = endpoints.GET_USER_FRAME
	param_dict = {"frame_id": frame_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp
	return result

def get_user_model(auth, model_identity, info=False):
	ep = endpoints.GET_USER_MODEL
	param_dict = {"model_identity": model_identity}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_user_models(auth, info=False):
	ep = endpoints.GET_USER_MODELS
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	models = resp.json()
	if "item" in models:
		models = models["item"]
	return models

def get_user_predictions(auth, info=False):
	ep = endpoints.GET_USER_PREDICTIONS
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	predictions = resp.json()
	if "item" in predictions:
		predictions = predictions["item"]
	return predictions

def import_module(auth, module_id, info=False):
	"""
	Import a module to the ecosystem-server.

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param module_id: The name of the module to be imported.
	"""
	ep = endpoints.IMPORT_MODULE
	param_dict = {"module_id": module_id}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def save_analysis(auth, analysis, info=False):
	ep = endpoints.SAVE_ANALYSIS
	resp = request_utils.create(auth, ep, json=analysis, info=info)
	response = resp.json()
	return response

def save_model(auth, model, info=False):
	ep = endpoints.SAVE_MODEL
	resp = request_utils.create(auth, ep, json=model, info=info)
	response = resp.json()
	return response

def save_prediction(auth, prediction, info=False):
	ep = endpoints.SAVE_PREDICTION
	resp = request_utils.create(auth, ep, json=prediction, info=info)
	response = resp.json()
	return response

def save_analysis(auth, analysis, info=False):
	ep = endpoints.SAVE_ANALYSIS
	resp = request_utils.create(auth, ep, json=analysis, info=info)
	response = resp.json()
	return response

def save_prediction_project(auth, prediction_project, info=False):
	ep = endpoints.SAVE_PREDICTION_PROJECT
	resp = request_utils.create(auth, ep, json=prediction_project, info=info)
	response = resp.json()
	return response

def save_user_deployments(auth, user_deployments, info=False):
	ep = endpoints.SAVE_USER_DEPLOYMENTS
	resp = request_utils.create(auth, ep, json=user_deployments, info=info)
	response = resp.json()
	return response

def save_user_frame(auth, user_frame, info=False):
	ep = endpoints.SAVE_USER_FRAME
	resp = request_utils.create(auth, ep, json=user_frame, info=info)
	response = resp.json()
	return response

def test_model(auth, value, info=False):
	ep = endpoints.TEST_PREDICTOR
	param_dict = {"value": value}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	response = resp.json()
	return response

def get_prediction_projects_base(auth, info=False):
	ep = endpoints.GET_PREDICTION_PROJECTS_BASE
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	response = resp.json()
	return response

def add_pretrained_model(auth, model_name, info=False):
	"""
	Add a pretrained h2o model to the ecosystem-server. The model zip file should be located in a models folder.

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param model_name: The name of the model to be added to the ecosystem-server.
	"""
	with open(f"models/{model_name}/experimental/modelDetails.json") as f:
		model_dict = json.load(f)
	model_dict["userid"] = "ecosystem"
	model_dict["model_identity"] = model_name
	save_model(auth, model_dict)
	deploy_predictor_config = {
		"deployment_id": model_name
		, "description": "Illustration of adding pre trained h2o model to the workbench"
		, "frame": model_dict["data_frame"]["name"]
		, "model": model_name
		, "from_model": f"{model_name}.zip"
		, "to_model": f"{model_name}.zip"
		, "version": "001"
		, "platform": "h2o"
		, "userid": "ecosystem"}
	deploy_predictor(auth, deploy_predictor_config)