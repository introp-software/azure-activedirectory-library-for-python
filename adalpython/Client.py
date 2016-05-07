from .httpclient import httpclient
import jwt
import urllib
import webbrowser
from urllib.parse import unquote, urlparse, urlencode, ParseResult, parse_qsl
import json
from adalpython import argument
import adalpython
from uuid import uuid1
from adalpython.argument import validate_string_param
import random
from string import ascii_lowercase
from adalpython.Storage import Storage
from random import choice
"""description of class"""
    
""" Need to add licensing terms here 
"""
class Client(object):
        
    def __init__(self):
     self._auth_end_point = _DefaultValues.auth_end_point
     self._resource = _DefaultValues.resource
     self._auth_flow = _DefaultValues.auth_flow
     self._clientsecret = _DefaultValues._clientsecret
     self._redirecturi = _DefaultValues.redirecturi
     self._clientid = _DefaultValues.client_id
     self._httpClient = None
     self._storage = None
 
    '''
     Perform an authorization request by redirecting resource owner's user agent to auth endpoint.
     
     Args:
      stateparams(List,optional) : Parameters to store as state.
      extraparams(List,optional) : Additional parameters to send with the OIDC request.
     
     '''
    def authrequest(self,requesttype,promptlogin = False,stateparams=[], extraparams=[]):
        validate_string_param(requesttype,'Request Type')
        try:
         url = self.get_login_url()
         params = self._get_authrequest_parameters(requesttype,promptlogin,stateparams,extraparams)
         url = self.add_url_params(url,params)
        except Exception as ex:
         return ex.args[0]
        webbrowser.open(url)

    ''' Handle auth response.
      Args:
       authparams(List) : Array of received auth response parameters.

      Returns:
      A dictionary with the following keys: 'IDToken' object, 'token parameters', 'stored state parameters'.
     
    '''
    def handle_auth_response(self,authparams):
     params = {'grant_type':'authorization_code'}
     try:
        if authparams['id_token'] is not None:
         res = {'id_token': authparams['id_token']}
         return res
     except:
            params['code'] = authparams['code']

     url = _DefaultValues.token_uri
     
     nonce = self._get_nonce_from_state(authparams['state'])

     if nonce is None:
         raise ValueError("Invalid state")



     params['client_id'] = self._get_clientid()
     params['client_secret'] = self._get_clientsecret()
     params['code'] = authparams['code']
     params['redirect_uri'] = self._get_redirecturi()
     httpClient = self._get_httpClient()
     response = httpClient.post(url,params)
     res = json.loads(response.content.decode('UTF-8'))
     return res

    '''/**
     * Process and return idtoken.
     *
     * @param string $idtoken Encoded id token.
     * @param string $expectednonce Expected nonce to validate received nonce against.
     * @return \microsoft\adalphp\OIDC\IDTokenInterface An IDToken object.
     */'''
    def process_idtoken(self,idtoken, expectednonce = ''):
        details = jwt.decode(idtoken,False,None,None)
        return details     

    '''
/**
     * Make a token request using the resource-owner credentials login flow.
     *
     * username The resource owner's username.
     * password The resource owner's password.
     * @return array Received parameters.
     */
     '''
    def rocredsrequest(self,username, password):
        url = _DefaultValues.token_uri
        parameters = {'grant_type':'password','scope':'openid profile email'}
        parameters['client_id'] = self._clientid
        parameters['client_secret'] = self._clientsecret
        parameters['resource'] = self._resource
        parameters['username'] = username
        parameters['password'] = password
        client = self._get_httpClient()
        res = client.post(url,parameters)
        return res

    def set_auth_end_point(self, value):
       self._auth_end_point = value
    
    def _get_auth_end_point(self):
       return self._auth_end_point
    
    def set_clientid(self, value):
       self._clientid = value
    
    def _get_clientid(self):
       return self._clientid
    
    def set_clientsecret(self, value):
       self._clientsecret = value
    
    def _get_clientsecret(self):
       return self._clientsecret
    
    def set_redirecturi(self, value):
       self._redirecturi = value
    
    def _get_redirecturi(self):
       return self._redirecturi
    
    def set_resource(self, value):
       self._resource = value
    
    def _get_resource(self):
       return self._resource
    
    def set_authflow(self, value):
       self._authflow = value
    
    def _get_authflow(self):
       return self._authflow

    def _get_httpClient(self):
       if self._httpClient is None:
           self._httpClient = httpclient()
       return self._httpClient

    def set_httpClient(self, value):
       self._httpClient = value

    def _get_authrequest_parameters(self,requesttype,promptlogin, stateparams, extraparams):
        params = {'scope':'openid'}
        params['client_id'] = self._get_clientid()
        params['redirect_uri'] = self._get_redirecturi()
        if requesttype == 'code' :
            params['response_type'] = 'code'
        else:
           if requesttype == 'code id_token':
            params['response_type'] = 'code id_token'
            params['nonce'] = '7Yfsaoier-oiuaoisudf'
           else:
            raise ValueError('Response type should be either \'code\' or \'code id_token\'.')
        params['response_mode'] = 'form_post'
        params['resource'] = self._get_resource()
        nonce = self._get_nonce()
        params['nonce'] = nonce
        state = self._get_new_state(nonce,stateparams)
        if promptlogin is True:
            params['prompt'] = 'login'

        stateparam = ''
        if stateparams is not None :            
         for stateitem in stateparams:
          stateparam = stateparam +"," + stateitem
            
        params['state'] = stateparam + state
        if extraparams is not None:
            for extra in extraparams:
                params[extra] = extra
        return params

    def get_login_url(self):
        if self._auth_end_point is None:
            return  "https://login.microsoftonline.com/common/oauth2/authorize"
        else:
            return self._get_auth_end_point()
        
    def _get_nonce(self):
        nonce = uuid1().hex.replace("-","")
        nonce = nonce+ self._get_random_string(40)
        return nonce


    def _get_new_state(self, nonce,additionalparam):
       state = self._get_random_string(15)
       storage = self._get_storage()
       storage.store_state(state,nonce,additionalparam)
       return state

    def _get_nonce_from_state(self,state):
       storage = self._get_storage()
       return storage.get_state(state)

    def _delete_state(self,state):
       storage = self._get_storage()
       storage.delete_state(state)

    def _get_random_string(self,length):
       return (''.join(choice(ascii_lowercase) for i in range(length)))

    def _get_storage(self):
        if self._storage is None:
            self._storage = Storage()
            self._storage.set_dbfile(self._storage_location)
           
        return self._storage

    def set_storage_location(self,value):
        self._storage_location = value

    def add_url_params(self,url, params):
     """ Add GET params to provided URL being aware of existing.

     :param url: string of target URL
     :param params: dict containing requested params to be added
     :return: string with updated URL
    """
     url = unquote(url)
     # Extracting url info
     parsed_url = urlparse(url)
     # Extracting URL arguments from parsed URL
     get_args = parsed_url.query
     # Converting URL arguments to dict
     parsed_get_args = dict(parse_qsl(get_args))
     # Merging URL arguments dict with new params
     parsed_get_args.update(params)
 
     # Bool and Dict values should be converted to json-friendly values
     # you may throw this part away if you don't like it :)
     parsed_get_args.update(
        {k: dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
     )

     # Converting URL argument to proper query string
     encoded_get_args = urlencode(parsed_get_args, doseq=True)
     # Creating new parsed result object based on provided with new
     # URL arguments. Same thing happens inside of urlparse.
     new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
     ).geturl()

     return new_url


class _DefaultValues:
    resource = 'https://management.core.windows.net/'
    auth_end_point = 'https://login.microsoftonline.com/common/oauth2/authorize'
    auth_flow = 'code'
    redirecturi = 'http://localhost'
    _clientsecret =''
    # This client is common to all tenants.  It is used by the Azure XPlat tools and is used for
    # username password logins.
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
    token_uri = "https://login.microsoftonline.com/common/oauth2/token"
