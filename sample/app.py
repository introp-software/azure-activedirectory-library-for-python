from flask import Flask, render_template, request
from adalpython import Client
import json
from flask import current_app
from storage import App_Storage



app = Flask(__name__)

app.config.from_pyfile('config.py')

#Configuration values, accessible across module.
secret_key = ''
client_id = ''
client_secret = ''
resource = ''
storage_location = ''
redirect_uri = ''

class User(object):
    """User object of application"""
    def __init__(self):
     Id = 0
     FirstName = ''
     LastName = ''
     Email = ''
     Password = ''
    
class Ad_user(object):
    def __init__(self):
     Id  = 0
     User_Id = 0
     Token = ''
     Token_Type = ''
     O365_Email = ''  

@app.route("/")
def my_form():
    try:
     return render_template("index1.html")
    except Exception as e:
     return e


@app.route("/login")
def login():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def my_form_post():
    username = request.form['username']
    password = request.form['password']
    try:
        read_configuration()
        client = Client()
        client.set_clientid(client_id)
        client.set_clientsecret(client_secret)
        client.set_resource(resource)
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


@app.route("/register", methods=['POST'])
def register():
    try:
        read_configuration()
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        user = User()
        user.Email = email
        user.FirstName = firstname
        user.LastName = lastname
        user.Password = password
        storage = App_Storage()
        user_id = storage.create_user(storage_location,user)
        return render_template('welcome.html', upn=user_id, firstname=firstname, lastname=lastname)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('welcome.html', upn=message, firstname=message, lastname=message)

@app.route("/authcode", methods=['POST'])
def authcode():
    try:
        client = Client()
        read_configuration()
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
        client.set_redirecturi(redirect_uri)
        client.set_clientid(client_id)
        client.set_clientsecret(client_secret)
        client.set_storage_location(storage_location)
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
    read_configuration()
    client = Client()
    client.set_clientid(client_id)
    client.set_redirecturi(redirect_uri)
    client.set_resource(resource)
    client.set_storage_location(storage_location)
    client.authrequest('code',promptUserToLogin)
    return  ""

@app.route("/hybrid", methods= ["POST"])
def get_token_using_code_id_token():
    promptUserToLogin = False
    client = Client()
    read_configuration()
    client.set_clientid(client_id)
    client.set_redirecturi(redirect_uri)
    client.set_resource(resource)
    client.authrequest('code id_token',promptUserToLogin)
    return  ""

@app.route("/locallogin", methods = ["POST"])
def locallogin():
    try:
     read_configuration()
     username = request.form["localemail"]
     password = request.form["localpassword"]
     storage = App_Storage()
     logged_in_user = storage.login_user(storage_location,username,password)
     return render_template('welcome.html', upn=logged_in_user[0], firstname=logged_in_user[2], lastname=logged_in_user[3])
    except Exception as ex:
     template = "An exception of type {0} occurred. Arguments:\n{1}"
     message = template.format(type(ex).__name__, ex.args)
     return render_template('welcome.html', upn=message, firstname=message, lastname=message)


def read_configuration():
    global secret_key,client_id,client_secret,resource,storage_location,redirect_uri
    secret_key = current_app.config['CLIENT_SECRET']
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET'] 
    resource = current_app.config['RESOURCE']
    storage_location = current_app.config['STORAGE_LOCATION']
    redirect_uri = current_app.config['REDIRECT_URI']

if __name__ == "__main__":
    app.run()