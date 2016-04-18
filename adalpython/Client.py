from adalpython.authentication_context import AuthenticationContext
class Client(object):
    """description of class"""
    
""" Need to add licensing terms here 

    Methods to be exposed:
    1. authrequest
    2. handle_auth_response
    3. process_idtoken
    4. tokenrequest
    5. handle_idtoken
    6. rocredsrequest
"""
def __init__(self):
    self._auth_end_point = _DefaultValues._auth_end_point
    self._resource = _DefaultValues.resource
    self._auth_flow = _DefaultValues.auth_flow
    self._client_secret = _DefaultValues.client_secret
    self._redirecturi = _DefaultValues.redirecturi
    self._clientid = _DefaultValues.client_id

'''
     Perform an authorization request by redirecting resource owner's user agent to auth endpoint.
     
     Args:
      stateparams(List,optional) : Parameters to store as state.
      extraparams(List,optional) : Additional parameters to send with the OIDC request.
      promptlogin(bool,optional) : Whether to prompt for login or use existing session.
     
     '''
def authrequest(stateparams=[], extraparams=[],promptlogin = False):
    return ""

''' Handle auth response.
      Args:
       authparams(List) : Array of received auth response parameters.

      Returns:
      A dictionary with the following keys: 'IDToken' object, 'token parameters', 'stored state parameters'.
     
     '''
def handle_auth_response(authparams):
    return ""

'''/**
     * Process and return idtoken.
     *
     * @param string $idtoken Encoded id token.
     * @param string $expectednonce Expected nonce to validate received nonce against.
     * @return \microsoft\adalphp\OIDC\IDTokenInterface An IDToken object.
     */'''
def process_idtoken(idtoken, expectednonce = ''):
     return ""

'''
  /**
     * Exchange an authorization code for an access token.
     *
     * @param string $code An authorization code.
     * @return array Received parameters.
     */
     '''
def tokenrequest(code):
    return ""

'''
/**
     * Handle auth response.
     *
     * @param array $authparams Array of received auth response parameters.
     * @return array List of IDToken object, array of token parameters, and stored state parameters.
     */
     '''
def handle_id_token(authparams):
     return ""

'''
/**
     * Make a token request using the resource-owner credentials login flow.
     *
     * username The resource owner's username.
     * password The resource owner's password.
     * @return array Received parameters.
     */
     '''
def rocredsrequest(username, password):
     context = AuthenticationContext(get_auth_end_point(), validate_authority)
     token_responses = []

def callback(err, token_response):
        if err:
            raise Exception("Error:{} token_response:{}".format(err, token_response))
        token_responses.append(token_response)

def token_func(context):
        context.token_request = TokenRequest(context._call_context, context, client_id, resource)
        context.token_request._get_token_with_username_password(username, password, callback)
        context._acquire_token(callback, token_func)
        return token_responses[0]

'''
1. AuthorizationEndPoint
2. ClientId
3. ClientSecret
4. RedirectURI
5. Resource
6. AuthFlow - Code or Code Access_Token
7. 
'''

def set_auth_end_point(self, value):
    self._auth_end_point = value

def get_auth_end_point(self):
    return self._auth_end_point

def set_clientid(self, value):
    self._clientid = value

def get_clientid(self):
    return self._clientid

def set_clientsecret(self, value):
    self._clientsecret = value

def get_clientsecret(self):
    return self._clientsecret

def set_redirecturi(self, value):
    self._redirecturi = value

def get_redirecturi(self):
    return self._redirecturi

def set_resource(self, value):
    self._resource = value

def get_resource(self):
    return self._resource

def set_authflow(self, value):
    self._authflow = value

def get_authflow(self):
    return self._authflow


class _DefaultValues:
    resource = 'https://management.core.windows.net/'
    auth_end_point = 'https://login.microsoftonline.com/common/oauth2/authorize'
    auth_flow = 'code'
    redirecturi = 'http://localhost'
    client_secret =''
    # This client is common to all tenants.  It is used by the Azure XPlat tools and is used for
    # username password logins.
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
