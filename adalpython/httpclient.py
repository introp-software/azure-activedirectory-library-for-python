import requests
class httpclient(object):
    """description of class
    TODO: Validate the input, and handle the exception."""
    def post(self,url,parameters,isJSON = False):
        if isJSON == True:
           response = requests.post(url,json=json.dumps(parameters))
        else:
           response = requests.post(url,data = parameters)

        return response


