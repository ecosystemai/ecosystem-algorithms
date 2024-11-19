from runtime.endpoints import data_management_engine as endpoints
from runtime import request_utils

# Data Management Engine
def update_dynamic_parameters(auth, json, info=False):
	ep = endpoints.UPDATE_DYNAMIC_PARAMETERS
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def update_dynamic_parameters_multi(auth, json, info=False):
	ep = endpoints.UPDATE_DYNAMIC_PARAMETERS_MULTI
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def rename_collection(auth, database, collection, new_collection, info=False):
	ep = endpoints.RENAME_COLLECTION
	param_dict = {
		"database": database,
		"collection": collection,
		"new_collection": new_collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_document_db_list(auth, server=None, info=False):
	ep = endpoints.GET_MONGO_DB_LIST
	if server == None:
		server = auth.get_server()
	param_dict = {
		"server": server
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_data(auth, database, collection, field, limit, projections, skip, info=False):
	"""
	Get data from a MongoDB collection using the find syntax.

	:param auth: Token for accessing the ecosystem-runtime. Created using access.
	:param database: Name of the database.
	:param collection: Name of the collection.
	:param field: The mongodb find search query.
	:param limit: The number of documents to return.
	:param projections: The fields to include or exclude in mongodb find query format.
	:param skip: The number of documents to skip.

	:return: A list of all documents matching the find criteria.
	"""
	ep = endpoints.GET_MONGO_DB_FIND
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"limit": limit,
		"projections": projections, 
		"skip": skip
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_data_sort(auth, database, collection, field, limit, projections, skip, sort, info=False):
	ep = endpoints.GET_MONGO_DB_FIND_SORT
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"limit": limit,
		"projections": projections, 
		"skip": skip,
		"sort": sort
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_document_db_collections(auth, database, info=False):
	ep = endpoints.GET_MONGO_DB_COLLECTIONS
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_cassandra(auth, sql, ctype, info=False):
	ep = endpoints.GET_CASSANDRA
	param_dict = {
		"sql": sql,
		"type": ctype
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_cassandra_version(auth, params, info=False):
	ep = endpoints.GET_CASSANDRA_FIND
	param_dict = {
		"params": params
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_cassandra_sql(auth, sql, info=False):
	ep = endpoints.GET_CASSANDRA_SQL
	param_dict = {
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def file_database_import(auth, file_name, database, collection, info=False):
	ep = endpoints.GET_CASSANDRA_SQL
	param_dict = {
		"file": file_name,
		"database": database,
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def delete_db_documents(auth, database, collection, search, info=False):
	ep = endpoints.DELETE_MONGO_DB_DOCUMENTS
	param_dict = {
		"database": database,
		"collection": collection,
		"search": search
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def create_document_collection_index(auth, database, collection, index, info=False):
	ep = endpoints.CREATE_MONGO_COLLECTION_INDEX
	param_dict = {
		"database": database,
		"collection": collection,
		"index": index
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def creat_index(auth, database, collection, index, info=False):
	ep = endpoints.CREATE_INDEX
	param_dict = {
		"database": database,
		"collection": collection,
		"index": index
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta