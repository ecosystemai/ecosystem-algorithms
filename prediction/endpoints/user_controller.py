# user-controller
USERS = {
	"type": "get",
	"endpoint": "/users",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}
POST_USERS = {
	"type": "post",
	"endpoint": "/users",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}
USERS_CURRENT = {
	"type": "get",
	"endpoint": "/users/current",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}