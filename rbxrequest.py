import requests
from time import sleep
from sys import exit
import json

#requests without session
def handleResponseCode(req):
    if req.status_code == 429:
        print("Ratelimit! waiting 1 min")
        sleep(60)
    elif req.status_code == 401:
        print("Bot's cookie has expired")
        exit()
    else:
        print(f"error. status code: {str(req.status_code)}")
        print("Request Headers: " + str(req.request.headers))
        #print("Request Body: " + str(req.request.body))
        print("Status Code: " + str(req.status_code))
        print("Response Headers: " + str(req.headers))
        print("Response Body: " + str(req.text))
        exit()

def request(method, url, decode_json=True, **kwargs):
    while True:
        req = requests.request(method, url, **kwargs)
        if req.status_code == 200:
            print(url)
            print(kwargs["headers"])
            return json.loads(req.text) if decode_json else req.text
        else:
            handleResponseCode(req)
            
def get(url, **kwargs):
    return request('get', url, **kwargs)
    
def post(url, **kwargs):
    return request('post', url, **kwargs)
            
def patch(url, **kwargs):
    return request('patch', url, **kwargs)

#custom session class
class session:
    def __init__(self, cookie):
        self.baseSession = requests.Session()
        self.baseSession.cookies[".ROBLOSECURITY"] = cookie
        self.baseSession.headers = {
            "accept": "application/json",
        }
        
    def handleResponseCode(self, req):
        if req.status_code == 403:
            print("Refreshed x-csrf-token")
            return
        else:
            handleResponseCode(req)
    
    def request(self, method, url, decode_json=True, **kwargs):
        while True:
            req = self.baseSession.request(method, url, **kwargs)
            if "X-CSRF-TOKEN" in req.headers:
                self.baseSession.headers["X-CSRF-TOKEN"] = req.headers["X-CSRF-TOKEN"]
                
            if req.status_code == 200:
                return json.loads(req.text) if decode_json else req.text
            else:
                self.handleResponseCode(req)
    
    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)
        
    def post(self, url, **kwargs):
        return self.request('post', url, **kwargs)
                
    def patch(self, url, **kwargs):
        return self.request('patch', url, **kwargs)
    
    def delete(self, url, **kwargs):
        return self.request('delete', url, **kwargs)