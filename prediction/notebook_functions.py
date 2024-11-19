import uuid
from IPython.display import display_javascript, display_html, display
import json
import pandas as pd
import matplotlib.pyplot as plt
from prediction.apis import worker_h2o
from prediction.apis import prediction_engine
import datetime

class RenderJSON(object):
	def __init__(self, json_data):
		if isinstance(json_data, dict):
			self.json_str = json.dumps(json_data)
		else:
			self.json_str = json_data
		self.uuid = str(uuid.uuid4())

	def _ipython_display_(self):
		display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid), raw=True)
		display_javascript("""
		require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
		document.getElementById('%s').appendChild(renderjson(%s))
		});
		""" % (self.uuid, self.json_str), raw=True)

def list_automl_models(model_data):
	sort_metric = model_data["leaderboard"]["sort_metric"]
	model_names = []
	for model in model_data["leaderboard"]["models"]:
		model_names.append(model["name"])

	model_metrics = model_data["leaderboard"]["sort_metrics"]

	df = pd.DataFrame(
		{
			"model_names": model_names,
			"model_metrics": model_metrics
		}
	)
	df.sort_values("model_metrics", inplace=True, ascending=False)
	return df

def show_automl_leaderboard(model_data, aml_name=None):
	sort_metric = model_data["leaderboard"]["sort_metric"]
	df = list_automl_models(model_data)
	ax = df.plot(y="model_metrics", x="model_names", kind="bar", align="center", alpha=0.5, legend=None)
	plt.xticks(rotation=90)
	ax.set_title("Performance of Models. Sorted Using Metric: {}".format(sort_metric))
	if aml_name != None:
		ax.set_title("{}: Performance of Models. Sorted Using Metric: {}".format(aml_name, sort_metric))
	ax.yaxis.grid(True)

def save_best_model(auth, df, rename=None):
	best_model_id = df.iloc[0]["model_names"]
	h2o_name = best_model_id
	_save_model(auth, h2o_name, df, rename)
	return h2o_name

def save_model(auth, h2o_model_name, df):
	_save_model(auth, h2o_model_name, df)
	return h2o_name

def _save_model(auth, h2o_name, df, rename):
	zip_name = h2o_name + ".zip"
	worker_h2o.download_model_mojo(auth, h2o_name)
	high_level_mojo = worker_h2o.get_train_model(auth, h2o_name, "single")
	model_to_save = high_level_mojo["models"][0]
	model_to_save["model_identity"] = h2o_name
	if rename != None:
		model_to_save["model_identity"] = rename
		model_to_save["model_id"]["name"] = rename
	model_to_save["userid"] = "user"
	model_to_save["timestamp"] = "time_stamp"

def show_variable_importance(stats):
	var_names = []
	for column in stats["columns"]:
		var_names.append(column["name"])
	# notebook_functions.RenderJSON(stats)
	df = pd.DataFrame(
		{
			var_names[0]: stats["data"][0],
			var_names[1]: stats["data"][1],
			var_names[2]: stats["data"][2],
			var_names[3]: stats["data"][3]
		}
	)
	return df

def save_file_as_userframe(auth, data_file, feature_store, user_name, columntypes=None):
	timestampvar = datetime.datetime.now().isoformat()
	data_file_prefix = ".".join(data_file.split(".")[:-1])
	hexframename = data_file_prefix + ".hex"
	imp = worker_h2o.file_to_frame(auth, data_file, 1, ",")
	descrip = "Automated feature store generated for " + feature_store
	frameID = feature_store
	if columntypes != None:
		for key in columntypes.keys():
				idx = imp["columnNames"].index(key)
				imp["columnTypes"][idx] = columntypes[key]
				imp["columnProperties"][idx]["new_type"] = columntypes[key] 
		
	str_imp = {
		"import": imp["import"],
		"parseSetup": imp["parseSetup"],
		"columnNames": imp["columnNames"],
		"columnTypes": imp["columnTypes"],
		"columnProperties": imp["columnProperties"]
	}
	str_imp = json.dumps(str_imp)
	user_frame = {
		"timestamp_parsed": timestampvar,
		"parser": "csv",
		"import": str_imp,
		"destination_frame": hexframename,
		"file_name": data_file,
		"description": descrip,
		"first_row_column_names": "1",
		"feature_store_script": "",
		"separator": "comma",
		"frame_id": frameID,
		"columnProperties": imp["columnProperties"],
		"created_by": user_name,
		"created_date": timestampvar,
		"preview_detail": {
			"summary": descrip,
			"image": "/data/xyz.png",
			"heading": frameID,
			"active": True,
			"detail": data_file
		}
	}

	worker_h2o.delete_frame(auth, hexframename)
	prediction_engine.save_user_frame(auth, user_frame)
	frame = worker_h2o.featurestore_to_frame(auth, user_frame)
	return frame["parseSetup"]["destination_frame"], imp