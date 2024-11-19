# Data Management Engine
UPDATE_DYNAMIC_PARAMETERS = {
	"type": "post",
	"endpoint": "/updateDynamicParameters",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
UPDATE_DYNAMIC_PARAMETERS_MULTI = {
	"type": "post",
	"endpoint": "/updateDynamicParametersMulti",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
RENAME_COLLECTION = {
	"type": "get",
	"endpoint": "/renameCollection",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_LIST = {
	"type": "get",
	"endpoint": "/getMongoDBList",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_FIND = {
	"type": "get",
	"endpoint": "/getMongoDBFind",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_FIND_SORT = {
	"type": "get",
	"endpoint": "/getMongoDBFindSort",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_COLLECTIONS = {
	"type": "get",
	"endpoint": "/getMongoDBCollections",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_CASSANDRA = {
	"type": "get",
	"endpoint": "/getCassandra",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_CASSANDRA_VERSION = {
	"type": "get",
	"endpoint": "/getCassandraVersion",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_CASSANDRA_SQL = {
	"type": "get",
	"endpoint": "/getCassandraSql",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
FILE_DATABASE_IMPORT = {
	"type": "get",
	"endpoint": "/fileDataImport",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DELETE_MONGO_DB_DOCUMENTS = {
	"type": "get",
	"endpoint": "/deleteMongoDBDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
CREATE_MONGO_COLLECTION_INDEX = {
	"type": "get",
	"endpoint": "/createMongoCollectionIndex",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
CREATE_INDEX = {
	"type": "get",
	"endpoint": "/createIndex",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}