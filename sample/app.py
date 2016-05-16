from flask import Flask, render_template, request, session
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
        session['firstname'] =  firstname
        session['lastname']= lastname
        session['email'] = email
        return render_template('user.html')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('user.html', upn=message, firstname=message, lastname=message)


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
        session['firstname'] =  firstname
        session['lastname']= lastname
        session['email'] = email
        session['userid'] = user_id
        return render_template('user.html')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('user.html', upn=message, firstname=message, lastname=message)

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
        session['firstname'] =  firstname
        session['lastname']= lastname
        session['email'] = upn
        return render_template('user.html')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('user.html', upn=message, firstname=message, lastname=message)

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
    client.set_storage_location(storage_location)
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
     try:
      ad_user = storage.get_ad_user(storage_location,logged_in_user[4])
     except LookupError:
      ad_user = None

     session['firstname'] =  logged_in_user[2]
     session['lastname']= logged_in_user[3]
     session['email'] = logged_in_user[0]
     session['userid'] = logged_in_user[4]
     return render_template('user.html', aduser = ad_user)
    except Exception as ex:
     template = "An exception of type {0} occurred. Arguments:\n{1}"
     message = template.format(type(ex).__name__, ex.args)
     return render_template('user.html', upn=message, firstname=message, lastname=message)

@app.route("/link", methods = ["POST"])
def linkaccount():
    try:
     email = session['email']
     promptUserToLogin = False
     client = Client()
     read_account_link_configuration()
     client.set_clientid(client_id)
     client.set_redirecturi(redirect_uri)
     client.set_resource(resource)
     client.set_storage_location(storage_location)
     stateparam = [email]
     client.authrequest('code id_token',promptUserToLogin,stateparam)
    except Exception as ex:
     template = "An exception of type {0} occurred. Arguments:\n{1}"
     message = template.format(type(ex).__name__, ex.args)
     return render_template('user.html', upn=message, firstname=message, lastname=message)

@app.route("/linkaccount", methods = ["POST"])
def linkaccountresponse():
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
    upn = token_details['upn']
    state = authResponse['state']
    if state.lower().find(upn.lower()) != -1:
     firstname = session['firstname']
     lastname =  session['lastname']
     app_storage = App_Storage()
     user = app_storage.get_user_by_email(storage_location,upn)
     ad_user = Ad_user()
     ad_user.User_Id = user[4]
     ad_user.Token = tokendetails['id_token']
     #ad_user.Token_Type = token_details['token_type']
     ad_user.O365_Email = upn
     app_storage.link_user(storage_location,user[4],ad_user)
     return render_template('user.html',aduser=ad_user)
    else:
     return render_template('user.html',error = "Your O365 email does not match with your current email id.")
   except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1}"
    message = template.format(type(ex).__name__, ex.args)
    return render_template('user.html', error = message)

@app.route("/unlink", methods = ["POST"])
def unlinkaccount():
    email = session['email']
    app_storage = App_Storage()
    app_storage.delink_user(storage_location,email)
    return render_template('user.html')

def read_configuration():
    global secret_key,client_id,client_secret,resource,storage_location,redirect_uri
    secret_key = current_app.config['CLIENT_SECRET']
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET'] 
    resource = current_app.config['RESOURCE']
    storage_location = current_app.config['STORAGE_LOCATION']
    redirect_uri = current_app.config['REDIRECT_URI']

def read_account_link_configuration():
    global secret_key,client_id,client_secret,resource,storage_location,redirect_uri
    secret_key = current_app.config['CLIENT_SECRET']
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET'] 
    resource = current_app.config['RESOURCE']
    storage_location = current_app.config['STORAGE_LOCATION']
    redirect_uri = current_app.config['LINK_REDIRECT_URI']

if __name__ == "__main__":
    app.secret_key = 'oiqauwre@098QUQR234)_02349H?'
    app.run()