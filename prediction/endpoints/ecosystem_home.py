GET_V1_HEALTH = {
	"type": "get",
	"endpoint": "/v1/health",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

POST_V1_HEALTH = {
	"type": "post",
	"endpoint": "/v1/health",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

PING = {
	"type": "get",
	"endpoint": "/ping",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

FLING = {
	"type": "get",
	"endpoint": "/fling",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}