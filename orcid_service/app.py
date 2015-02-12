from flask import Flask
from flask import current_app, request
from flask.ext.discoverer import Discoverer, advertise
import config
import requests

app = Flask(__name__, static_folder=None)
discoverer = Discoverer(app)

@advertise(scopes=['ads:default'], methods=['OPTIONS', 'GET'])
@app.route('/exchangeOAuthCode')
def getAccessToken():
    '''Exchange 'code' for 'access_token' data'''
    payload = dict(request.args)
    if 'code' not in payload:
        raise Exception('Parameter code is missing')
    headers = dict(Accept='application/json')
    data = {
      'client_id': config.ORCID_CLIENT_ID,
      'client_secret': config.ORCID_CLIENT_SECRET,
      'code': payload['code'][0],
      'grant_type': 'authorization_code'
    }
    r = requests.post(config.ORCID_API_ENDPOINT + '/oauth/token', data=data, headers=headers)
    return r.text, r.status_code

@advertise(scopes=['ads:default'], methods=['OPTIONS', 'GET'])
@app.route('/query')
def query():
    '''docstring for route2'''
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)