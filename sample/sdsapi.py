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
from token_helper import token_helper
import requests
import json
from werkzeug.routing import ValidationError

class sdsapi(object):
    """This class handles the calls to SDS api."""
    def __init__(self, **kwargs):
      return super().__init__(**kwargs)
  
    def getschoollist(self,token):
     tokenhelper = token_helper(token)
     response = {}
     response['success'] = False
     token = tokenhelper.get_token()
     if (token is None):
       response['value'] = "The access token to fetch sds data may be expired or not present.Please login through Microsoft account using method Auth Code or Credentials."
       return response
     else:
      options = {}
      headers = {"Authorization" : "Bearer "+ token}
      #options['headers'] = headers
      url = "https://graph.windows.net/cdsync66.onmicrosoft.com/administrativeUnits?api-version=beta&$filter=extension_fe2174665583431c953114ff7268b7b3_Education_ObjectType%20eq%20'School'"
      response_str = requests.get(url,headers = headers)
      response['value'] = self.parse_sdsapi_response(response_str)
      response['success'] = True
      return response
 

    def parse_sdsapi_response(self,response):
     result = json.loads(response.content.decode('utf-8'))
     if (result is None):
        raise ValidationError('Error : Bad api call')
          
     try: 
      if (result['odata.error'] is not None):
        if ((result['odata.error']['message']) is not None and (result['odata.error']['message']['value'] is not None)):
            apierrormessage = result['odata.error']['message']['value'];
            raise ValidationError(apierrormessage)
        else:
            raise ValidationError('Error : Bad api call')
     except KeyError:
      values = {}
      properties = result['value']
      for key in properties[0]:
         new_key = key.replace('extension_fe2174665583431c953114ff7268b7b3_','')
         values[new_key] = properties[0][key]
      return values

       
       




