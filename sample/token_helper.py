 #Copyright (c) 2016 Micorosft Corporation

 #Permission is hereby granted, free of charge, to any person obtaining a copy
 #of this software and associated documentation files (the "Software"), to deal
 #in the Software without restriction, including without limitation the rights
 #to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 #copies of the Software, and to permit persons to whom the Software is
 #furnished to do so, subject to the following conditions:

 #The above copyright notice and this permission notice shall be included in
 #all copies or substantial portions of the Software.

 #THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 #THE SOFTWARE.

 # @author Prasanna Mategaonkar <prasanna@introp.net>
 # @license MIT
 # @copyright (C) 2016 onwards Microsoft Corporation (http://microsoft.com/)

from storage import app_storage
from localuser import user
from localaduser import ad_user
import time
from urllib.parse import unquote, urlparse, urlencode, ParseResult, parse_qsl
from flask import current_app
from adalpython import httpclient, Client
import json


class token_helper(object):
    """description of class"""

    rawtoken = ''
    httpclient = None

    def __init__(self,token):
        self.rawtoken = token

    def is_token_valid(self):
        if (self.rawtoken is None or
            int(self.rawtoken['expires_on']) < int(round(time.time() * 1000))):
         return False
        else:
         return True

    def get_token(self):
     try:
      if(self.is_token_valid() == True):
         return self.rawtoken["access_token"]
      else:
         self.refresh_token()
         return self.rawtoken["access_token"]
     except Exception as ex:
      return None

    def refresh_token(self):
        params = {}
        params['client_id'] = current_app.config['CLIENT_ID']
        params['client_secret'] = current_app.config['CLIENT_SECRET']
        params['redirect_uri'] = current_app.config['REDIRECT_URI']
        params['grant_type'] = 'refresh_token'
        params['refresh_token'] = self.rawtoken['refresh_token']
        params['resource'] = current_app.config['RESOURCE']
        #url = self.add_url_params(,params)
        httpClient = httpclient()
        response = httpClient.post('https://login.microsoftonline.com/common/oauth2/token',params)
        res = json.loads(response.content.decode('UTF-8'))
        ad_userobj = ad_user()
        client = Client()
        ad_userobj.Token = res
        id_token = res['access_token']
        token_details = client.process_idtoken(id_token)
        ad_userobj.O365_Email = token_details['upn']
        appstorage = app_storage()
        appstorage.update_ad_user(current_app.config['STORAGE_LOCATION'],ad_userobj)
        self.rawtoken = res
            
      

         