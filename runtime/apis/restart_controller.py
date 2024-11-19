from runtime.endpoints import restart_controller as endpoints
from runtime import request_utils

def restart(auth, info=False):
# Restart the server
    ep = endpoints.RESTART
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.json()
    return meta

def restart_app(auth, info=False):
# Restart using actuator
    ep = endpoints.RESTART_APP
    resp = request_utils.create(auth, ep, info=info)
    meta = resp.json()
    return meta
