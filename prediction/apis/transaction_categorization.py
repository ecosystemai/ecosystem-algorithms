from prediction.endpoints import transaction_categorization as endpoints
from prediction import request_utils

def get_transactions(auth, json, info=False):
	ep = endpoints.GET_TRANSACTIONS
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def get_transactions_cat_predicted(auth, json, info=False):
	ep = endpoints.GET_TRANSACTIONS_CAT_PREDICTED
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def get_transactions_processed(auth, count, info=False):
	ep = endpoints.GET_TRANSACTIONS_PROCESSED
	param_dict = {"count": count}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	transactions = resp.json()
	if "items" in transactions:
		transactions = transactions["items"]
	return transactions