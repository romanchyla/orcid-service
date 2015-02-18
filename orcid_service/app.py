from flask import Flask
from flask import current_app, request
from flask.ext.discoverer import Discoverer, advertise
import config
import requests

app = Flask(__name__, static_folder=None)
discoverer = Discoverer(app)

@advertise(scopes=['ads:default'], methods=['OPTIONS', 'GET'])
@app.route('/exchangeOAuthCode', methods=['GET'])
def getAccessToken():
    '''Exchange 'code' for 'access_token' data'''
    payload = dict(request.args)
    if 'code' not in payload:
        raise Exception('Parameter code is missing')
    headers = {'Accept': 'application/json'}
    data = {
      'client_id': config.ORCID_CLIENT_ID,
      'client_secret': config.ORCID_CLIENT_SECRET,
      'code': payload['code'][0],
      'grant_type': 'authorization_code'
    }
    #print config.ORCID_OAUTH_ENDPOINT, data, headers
    r = requests.post(config.ORCID_OAUTH_ENDPOINT, data=data, headers=headers)
    return r.text, r.status_code

@advertise(scopes=['ads:default'], methods=['OPTIONS', 'GET', 'POST'])
@app.route('/<orcid_id>/orcid-profile', methods=['GET', 'POST'])
def orcidProfile(orcid_id):
    '''Get/Set /[orcid-id]/orcid-profile - all communication exclusively in JSON'''
    payload, headers = check_request(request)
    if request.method == 'GET':
        r = requests.get(config.ORCID_API_ENDPOINT + '/' + orcid_id + '/orcid-profile',
                         headers=headers)
    else:
        r = requests.post(config.ORCID_API_ENDPOINT + '/' + orcid_id + '/orcid-profile',
                         json=payload, headers=headers)
    return r.text, r.status_code

@advertise(scopes=['ads:default'], methods=['OPTIONS', 'GET', 'POST', 'PUT'])
@app.route('/<orcid_id>/orcid-works', methods=['GET', 'POST', 'PUT'])
def orcidWorks(orcid_id):
    '''Get/Set /[orcid-id]/orcid-works - all communication exclusively in JSON'''
    
    payload, headers = check_request(request)
    
    if request.method == 'GET':
        r = requests.get(config.ORCID_API_ENDPOINT + '/' + orcid_id + '/orcid-works', 
                      headers=headers)
    elif request.method == 'PUT':
        r = requests.put(config.ORCID_API_ENDPOINT + '/' + orcid_id + '/orcid-works', 
                      json=payload, headers=headers)
    elif request.method == 'POST':
        r = requests.post(config.ORCID_API_ENDPOINT + '/' + orcid_id + '/orcid-works', 
                      json=payload, headers=headers)
    return r.text, r.status_code

    

def check_request(request):
    
    headers = dict(request.headers)
    if 'Orcid-Authorization' not in headers:
        raise Exception('Header Orcid-Authorization is missing')
    h = {
         'Accept': 'application/json', 
         'Authorization': headers['Orcid-Authorization'],
         'Content-Type': 'application/json'
         }
    # transfer headers from the original
    #for x in ['Content-Type']:
    #    if x in headers:
    #        h[x] = headers[x]
            
    if request.json:
        payload = request.json
    else:
        payload = dict(request.args)
        payload.update(dict(request.form))
    
    return (payload, h)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)
