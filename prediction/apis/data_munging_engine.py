from prediction.endpoints import data_munging_engine as endpoints
from prediction import request_utils
# from prediction.apis import quickflat as qf

def concat_columns2(auth, database, collection, attribute, separator, info=False):
	ep = endpoints.CONCAT_COLUMNS2
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"separator": separator
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_date2(auth, database, collection, attribute, find, info=False):
	ep = endpoints.DATE_ENRICH2
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def auto_normalize_all(auth, database, collection, fields, find, normalized_high, normalized_low, info=False):
	ep = endpoints.AUTO_NORMALIZE_ALL
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"fields": fields,
		"find": find,
		"normalizedHigh": normalized_high,
		"normalizedLow": normalized_low
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def concat_columns(auth, databasename, collection, attribute, info=False):
	ep = endpoints.CONCAT_COLUMNS
	param_dict = {"mongodb": databasename, "collection": collection, "attribute": attribute}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_date(auth, database, collection, attribute, info=False):
	ep = endpoints.DATE_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enum_convert(auth, database, collection, attribute, info=False):
	ep = endpoints.ENUM_CONVERT
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def fill_zeros(auth, database, collection, attribute, info=False):
	ep = endpoints.FILL_ZEROS
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def fill_values(auth, database, collection, find, attribute, value, info=False):
	ep = endpoints.FILL_VALUES
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"find": find,
		"attribute": attribute,
		"value": value
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta


def foreign_key_aggregator(auth, database, collection, attribute, search, mongodbf, collectionf, attributef, fields, info=False):
	ep = endpoints.FOREIGN_KEY_AGGREGATOR
	param_dict = {
		"mongodb": database,
		"collection": collection,
		"attribute": attribute,
		"search": search,
		"mongodbf": mongodbf,
		"collectionf": collectionf,
		"attributef": attributef,
		"fields": fields
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def foreign_key_lookup(auth, database, collection, attribute, search, mongodbf, collectionf, attributef, fields, info=False):
	ep = endpoints.FOREIGN_KEY_LOOKUP
	param_dict = {
		"mongodb": database,
		"collection": collection,
		"attribute": attribute,
		"search": search,
		"mongodbf": mongodbf,
		"collectionf": collectionf,
		"attributef": attributef,
		"fields": fields
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_fragments(auth, database, collection, attribute, strings, info=False):
	ep = endpoints.FRAGMENT_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"stringOnly": strings
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_fragments2(auth, database, collection, attribute, strings, find, info=False):
	ep = endpoints.FRAGMENT_ENRICH2
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"stringOnly": strings,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def generate_features(auth, database, collection, featureset, categoryfield, datefield, numfield, groupby, find, info=False):
	ep = endpoints.GENERATE_FEATURES
	param_dict = {"database": database, "collection": collection, "featureset":featureset, "categoryfield":categoryfield, "datefield":datefield, "numfield":numfield, "groupby":groupby, "find":find}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def generate_features_normalize(auth, database, collection, find, inplace, normalized_high, normalized_low, numfields, info=False):
	ep = endpoints.GENERATE_FEATURES_NORMALIZE
	param_dict = {"database": database, "collection": collection, "find":find, "inPlace": inplace, "normalizedHigh": normalized_high, "normalizedLow": normalized_low, "numfields": numfields}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def get_categories(auth, database, collection, categoryfield, find, total, info=False):
	ep = endpoints.GET_CATEGORIES
	param_dict = {"database": database, "collection":collection, "categoryfield":categoryfield, "total": total, "find": find}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def get_categories_ratio(auth, database, collection, categoryfield, find, total, info=False):
	ep = endpoints.GET_CATEGORIES_RATIOS
	param_dict = {"database": database, "collection":collection, "categoryfield":categoryfield, "total": total, "find": find}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_location(auth, database, collection, attribute, info=False):
	ep = endpoints.LOCATION_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_mcc(auth, database, collection, attribute, find, info=False):
	ep = endpoints.MCC_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def prediction_enrich_fast(auth, database, collection, search, sort, predictor, predictor_label, attributes, skip, limit, info=False):
	ep = endpoints.PREDICTION_ENRICH_FAST_GET
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"search": search,
		"sort": sort,
		"predictor": predictor,
		"predictor_label": predictor_label,
		"attributes": attributes,
		"skip": skip,
		"limit": limit
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta
	
# predicition_enrich(auth, database, collection2, search, sort, predictor, predictor_label, attributes) 
def predicition_enrich(auth, database, collection, search, sort, predictor, predictor_label, attributes, info=False):
	ep = endpoints.PREDICTION_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"search": search,
		"predictor": predictor,
		"predictor_label": predictor_label,
		"attributes": attributes,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_sic(auth, database, collection, attribute, find, info=False):
	ep = endpoints.SIC_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

# def quickflat(config, info=False):
# 	quick_flat = qf.QuickFlat(config)
# 	quick_flat.flatten()

def process_client_pulse_reliability(auth, collection, collectionOut, database, find, groupby, mongoAttribute, typeName, info=False):
	ep = endpoints.PROCESS_CLIENT_PULSE_RELIABILITY
	param_dict = {
		"collection": collection,
		"collectionOut": collectionOut,
		"database": database,
		"find": find,
		"groupby": groupby,
		"mongoAttribute": mongoAttribute,
		"type": typeName
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def generate_time_series_features(auth, categoryfield, collection, database, datefield, featureset, find, groupby, numfield, startdate=None, windowsize=1, info=False):
	ep = endpoints.GENERATE_TIME_SERIES_FEATURES
	param_dict = {
		"categoryfield": categoryfield,
		"collection": collection,
		"database": database,
		"datefield": datefield,
		"featureset": featureset,
		"find": find,
		"groupby": groupby,
		"numfield": numfield,
		"startdate": startdate,
		"windowsize": windowsize
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def personality_enrich(auth, category, collection, collectionOut, database, find, groupby, info=False):
	ep = endpoints.PERSONALITY_ENRICH
	param_dict = {
		"category": category,
		"collection": collection,
		"collectionOut": collectionOut,
		"database": database,
		"find": find,
		"groupby": groupby		
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def munge_transactions_aggregate(auth, munging_step, project_id, info=False):
	ep = endpoints.MUNGE_TRANSACTIONS_AGGREGATE
	param_dict = {
		"munging_step": munging_step,
		"project_id": project_id
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def munge_transactions(auth, munging_step, project_id, info=False):
	ep = endpoints.MUNGE_TRANSACTIONS
	param_dict = {
		"munging_step": munging_step,
		"project_id": project_id
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def flatten_document(auth, db, collection, attribute, find, info=False):
	ep = endpoints.FLATTEN_DOCUMENT
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def delete_key(auth, db, collection, attribute, find, info=False):
	ep = endpoints.DELETE_KEY
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def delete_many_documents(auth, db, collection, find, info=False):
	ep = endpoints.DELETE_MANY_DOCUMENTS
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def process_range(auth, db, collection, attribute, new_attribute, find, rules, info=False):
	ep = endpoints.PROCESS_RANGE
	param_dict = {
		"database": db,
		"collection": collection,
		"mongoAttribute": attribute,
		"newAttribute": new_attribute,
		"find": find,
		"rules": rules
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def nlp_worker(auth, database, collection, database_out, collection_out, attribute, find, model="original", summarization_max=10, summarization_min=5, transformer="t5-small", model_type="nlp_b5_base", info=False):
	ep = endpoints.NLP_WORKER
	param_dict = {
		"database": db,
		"collection": collection,
		"database_out": database_out,
		"collection_out": collection_out,
		"attribute": attribute,
		"find": find,
		"model": model,
		"summarization_max": summarization_max,
		"summarization_min": summarization_min,
		"transformer": transformer,
		"type": model_type,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def delete_many_documents(auth, db, collection, find, info=False):
	ep = endpoints.DELETE_MANY_DOCUMENTS
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def process_range(auth, db, collection, find, attribute, new_attribute, rules, info=False):
	ep = endpoints.PROCESS_RANGE
	param_dict = {
		"database": db,
		"collection": collection,
		"find": find,
		"mongoAttribute": attribute,
		"newAttribute": new_attribute,
		"rules": rules
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta


def prediction_enrich_fast_post(auth, json, info=False):
	ep = endpoints.PREDICTION_ENRICH_FAST_POST
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result