from flask import Flask, render_template, request
from adalpython import Client
import json

app = Flask(__name__)


@app.route("/")
def my_form():
    return render_template("index1.html")


@app.route("/login")
def login():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def my_form_post():
    username = request.form['username']
    password = request.form['password']
    try:
        # print(help(adal))
        # 'https://login.microsoftonline.com/common'
        client = Client()
        client.set_clientid('445d81db-d520-4e5e-8713-ffedcb7ab79f')
        client.set_clientsecret('SmDf3Vn4xHcDBlrbOMwufPckAFymWFSfIWLKX4rrMpE=')
        client.set_resource('https://graph.windows.net')
        token_response = client.rocredsrequest(username, password)
        res = json.loads(token_response.content.decode('UTF-8'))
        access_token = res['access_token']
        id_token = res['id_token']
        token_details = client.process_idtoken(id_token)
        firstname = token_details['given_name']
        lastname = token_details['family_name']
        upn = token_details['upn']
        return render_template('welcome.html', upn=upn, firstname=firstname, lastname=lastname)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('welcome.html', upn=message, firstname=message, lastname=message)


@app.route("/authcode", methods=['POST'])
def authcode():
    try:
        client = Client()
        authResponse = {}

        try:
            if request.form['id_token'] is not None:
                authResponse['id_token'] = request.form['id_token']
            else:
                authResponse['code'] = request.form['code']
        except:
            authResponse['code'] = request.form['code']

        authResponse['state'] = request.form['state']
        authResponse['session_state'] = request.form['session_state']
        client.set_redirecturi("http://localhost:5000/authcode")
        client.set_clientid('445d81db-d520-4e5e-8713-ffedcb7ab79f')
        client.set_clientsecret('SmDf3Vn4xHcDBlrbOMwufPckAFymWFSfIWLKX4rrMpE=')
        client.set_storage_location("G:\\Dev\\FlaskApp\\test.sqlite")
        tokendetails = client.handle_auth_response(authResponse)
        id_token = tokendetails['id_token']
        token_details = client.process_idtoken(id_token)
        firstname = token_details['given_name']
        lastname = token_details['family_name']
        upn = token_details['upn']
        return render_template('welcome.html', upn=upn, firstname=firstname, lastname=lastname)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('welcome.html', upn=message, firstname=message, lastname=message)

@app.route("/usecode", methods= ["POST"])
def get_token_using_code():
    promptUserToLogin = False
    client = Client()
    client.set_clientid('445d81db-d520-4e5e-8713-ffedcb7ab79f')
    client.set_redirecturi("http://localhost:5000/authcode")
    client.set_resource("https://graph.windows.net")
    client.set_storage_location("G:\\Dev\\FlaskApp\\test.sqlite")
    client.authrequest('code',promptUserToLogin)
    return  ""

@app.route("/hybrid", methods= ["POST"])
def get_token_using_code_id_token():
    promptUserToLogin = False
    client = Client()
    client.set_clientid('445d81db-d520-4e5e-8713-ffedcb7ab79f')
    client.set_redirecturi("http://localhost:5000/authcode")
    client.set_resource("https://graph.windows.net")
    client.authrequest('code id_token',promptUserToLogin)
    return  ""
if __name__ == "__main__":
    app.run()
