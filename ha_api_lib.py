import secrets
import requests
import json

class endpoints:
    def status():
        return str(secrets.ha_url).strip('/')+"/api"
    def config():
        return str(secrets.ha_url).strip('/')+"/api/config"
    def events():
        return str(secrets.ha_url).strip('/')+"/api/events"
    def services():
        return str(secrets.ha_url).strip('/')+"/api/services"
    def states(entity_id=None):
        if(entity_id == None):
            return str(secrets.ha_url).strip('/')+"/api/states"
        else:
            return str(secrets.ha_url).strip('/')+"/api/states/" + str(entity_id)

class payload:
    def headers():
        headers =  {
            "Authorization": "Bearer "+secrets.ha_token,
            "content-type": "application/json",
        }
        return headers

class entities:
    def all():
        url = endpoints.states()
        headers = payload.headers()
        print(url)
        print(headers)
        states = requests.get(url, headers=headers).json()
        return states
    def entity_id(entity_id):
        url = endpoints.states(entity_id)
        headers = payload.headers()
        print(url)
        print(headers)
        states = requests.get(url, headers=headers).json()
        return states

