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
            
      

         

    #def add_url_params(self,url, params):
    # """ Add GET params to provided URL being aware of existing.

    # :param url: string of target URL
    # :param params: dict containing requested params to be added
    # :return: string with updated URL
    #"""
    # url = unquote(url)
    # # Extracting url info
    # parsed_url = urlparse(url)
    # # Extracting URL arguments from parsed URL
    # get_args = parsed_url.query
    # # Converting URL arguments to dict
    # parsed_get_args = dict(parse_qsl(get_args))
    # # Merging URL arguments dict with new params
    # parsed_get_args.update(params)
 
    # # Bool and Dict values should be converted to json-friendly values
    # # you may throw this part away if you don't like it :)
    # parsed_get_args.update(
    #    {k: dumps(v) for k, v in parsed_get_args.items()
    #     if isinstance(v, (bool, dict))}
    # )

    # # Converting URL argument to proper query string
    # encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # # Creating new parsed result object based on provided with new
    # # URL arguments. Same thing happens inside of urlparse.
    # new_url = ParseResult(
    #    parsed_url.scheme, parsed_url.netloc, parsed_url.path,
    #    parsed_url.params, encoded_get_args, parsed_url.fragment
    # ).geturl()

    # return new_url
