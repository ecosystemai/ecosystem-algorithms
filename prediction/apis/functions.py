import datetime
from prediction.apis import worker_h2o
from prediction.apis import prediction_engine
import json

def save_file_as_userframe(auth, data_file, feature_store, user_name):
	timestampvar = datetime.datetime.now().isoformat()
	data_file_prefix = ".".join(data_file.split(".")[:-1])
	hexframename = data_file_prefix + ".hex"
	imp = worker_h2o.file_to_frame(auth, data_file, 1, ",")
	# ['import', 'parseSetup', 'columnNames', 'columnTypes', 'columnProperties'
	descrip = "Automated feature store generated for " + feature_store
	frameID = feature_store
	str_imp = {
		"import": imp["import"],
		"parseSetup": imp["parseSetup"],
		"columnNames": imp["columnNames"],
		"columnTypes": imp["columnTypes"],
		"columnProperties": imp["columnProperties"]
	}
	str_imp = json.dumps(str_imp)
	# str_imp = str(str_imp).replace("'", '"').replace("None", "null").replace("False", "false").replace("True", "true")
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

def get_list_of_fields(db, collection):
	fields_pipeline = [
		{"$project":{"arrayofkeyvalue":{"$objectToArray":"$$ROOT"}}},
		{"$unwind":"$arrayofkeyvalue"},
		{"$group":{"_id":None,"allkeys":{"$addToSet":"$arrayofkeyvalue.k"}}}
	]
	cursor = db[collection].aggregate(fields_pipeline)
	doc = cursor.next()
	list_of_fields = doc["allkeys"]
	if "_id" in list_of_fields: list_of_fields.remove("_id")
	return list_of_fields