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
from flask import Flask, render_template, request, session
import json
from flask import current_app
from localuser import user
from localaduser import ad_user
from storage import app_storage
from sdsapi import sdsapi
from adalpython import Client, httpclient
from adalpython.httpclient import httpclient



app = Flask(__name__)

app.config.from_pyfile('config.py')

#Configuration values, accessible across module.
secret_key = ''
client_id = ''
client_secret = ''
resource = ''
storage_location = 'aadpythonstorage.sqlite'
redirect_uri = ''

 

@app.route("/")
def my_form():
    try:
     return render_template("Index.html")
    except Exception as e:
     return e


@app.route("/login")
def login():
    return render_template("Login.html")

@app.route("/logout")
def logout():
    session.logged_in = False
    return render_template("Index.html")

@app.route("/", methods=['POST'])
def my_form_post():
    username = request.form['username']
    password = request.form['password']
    try:
        read_configuration()
        client =  Client()
        client.set_clientid(client_id)
        client.set_clientsecret(client_secret)
        client.set_resource(resource)
        token_response = client.rocredsrequest(username, password)
        res = json.loads(token_response.content.decode('UTF-8'))
        access_token = res['access_token']
        id_token = res['id_token']
        token_details = client.process_idtoken(id_token)
        try:
            firstname = token_details['given_name']
            lastname = token_details['family_name']
        except KeyError:
            firstname = token_details['name']
            lastname = ''

        upn = token_details['upn']
        appstorage = app_storage()
        try:
         ad_userobj = appstorage.get_ad_user_by_email(storage_location,upn) 
         ad_userobj.Token = res;
         appstorage.update_ad_user(storage_location,ad_userobj)
        except LookupError:
         ad_userobj = ad_user()
         ad_userobj.O365_Email = upn
         ad_userobj.Token = res
         appstorage.create_ad_user(storage_location,ad_userobj)

        sdsapiobj = sdsapi()
        sdsapiobj.getschoollist(res)
        session['firstname'] =  firstname
        session['lastname']= lastname
        session['email'] = email
        session.logged_in = True
        return render_template('User.html')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('Login.html', error = message)


@app.route("/register", methods=['POST'])
def register():
    try:
        read_configuration()
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        localuser = user()
        localuser.Email = email
        localuser.FirstName = firstname
        localuser.LastName = lastname
        localuser.Password = password
        storage = app_storage()
        user_id = storage.create_user(storage_location,localuser)
        sdsapiobj = sdsapi()
        sdsresponse = sdsapiobj.getschoollist(None)
        session['sdsresponse'] = sdsresponse
        session['firstname'] =  firstname
        session['lastname']= lastname
        session['email'] = email
        session['userid'] = user_id
        session.logged_in = True
        return render_template('User.html')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('Login.html', error=message)

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
        try:
            firstname = token_details['given_name']
            lastname = token_details['family_name']
        except KeyError:
            firstname = token_details['name']
            lastname = ''

        upn = token_details['upn']
        appstorage = app_storage()
        try:
         ad_userobj = appstorage.get_ad_user_by_email(storage_location,upn) 
         ad_userobj.Token = tokendetails;
         appstorage.update_ad_user(storage_location,ad_userobj)
        except LookupError:
         ad_userobj = ad_user()
         ad_userobj.O365_Email = upn
         ad_userobj.Token = tokendetails
         appstorage.create_ad_user(storage_location,ad_userobj)

        sdsapiobj = sdsapi()
        sdsresponse = sdsapiobj.getschoollist(tokendetails)
        session['sdsresponse'] = sdsresponse
        session['firstname'] =  firstname
        session['lastname']= lastname
        session['email'] = upn
        session.logged_in = True
        return render_template('User.html')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1}"
        message = template.format(type(ex).__name__, ex.args)
        return render_template('Login.html', error=message)

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
    return  "PlaceHolder.html"

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
    return  "PlaceHolder.html"

@app.route("/locallogin", methods = ["POST"])
def locallogin():
    try:
     read_configuration()
     username = request.form["localemail"]
     password = request.form["localpassword"]     
     storage = app_storage()
     logged_in_user = storage.login_user(storage_location,username,password)
     try:
      ad_user = storage.get_ad_user(storage_location,logged_in_user[4])
     except LookupError:
      ad_user = None

     sdsapiobj = sdsapi()
     sdsresponse = sdsapiobj.getschoollist(None)
     session['sdsresponse'] = sdsresponse
     session['firstname'] =  logged_in_user[2]
     session['lastname']= logged_in_user[3]
     session['email'] = logged_in_user[0]
     session['userid'] = logged_in_user[4]
     session.logged_in = True
     return render_template('User.html', aduser = ad_user)
    except Exception as ex:
     template = "{0}"
     message = template.format(ex.args)
     return render_template('Login.html', error = message)

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
     client.authrequest('code',promptUserToLogin,stateparam)
    except Exception as ex:
     template = "An exception of type {0} occurred. Arguments:\n{1}"
     message = template.format(type(ex).__name__, ex.args)
     return render_template('User.html',error = message)

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
     app_storageObj = app_storage()
     user = app_storageObj.get_user_by_email(storage_location,upn)
     ad_userobj = ad_user()
     ad_userobj.User_Id = user[4]
     ad_userobj.Token = tokendetails
     #ad_user.Token_Type = token_details['token_type']
     ad_userobj.O365_Email = upn
     app_storage.link_user(storage_location,user[4],ad_userobj)
     session.logged_in = True
     return render_template('User.html',aduser=ad_userobj)
    else:
     session.logged_in = True
     return render_template('User.html',error = "Your O365 email does not match with your current email id.")
   except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1}"
    message = template.format(type(ex).__name__, ex.args)
    session.logged_in = True
    return render_template('User.html', error = message)

@app.route("/unlink", methods = ["POST"])
def unlinkaccount():
    email = session['email']
    read_configuration()
    app_storage = App_Storage()
    app_storage.delink_user(storage_location,email)
    session.logged_in = True
    return render_template('User.html')


def read_configuration():
    global secret_key,client_id,client_secret,resource,storage_location,redirect_uri
    #secret_key = current_app.config['CLIENT_SECRET']
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET'] 
    resource = current_app.config['RESOURCE']
    redirect_uri = current_app.config['REDIRECT_URI']

def read_account_link_configuration():
    global secret_key,client_id,client_secret,resource,storage_location,redirect_uri
    #secret_key = current_app.config['CLIENT_SECRET']
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET'] 
    resource = current_app.config['RESOURCE']
    redirect_uri = current_app.config['LINK_REDIRECT_URI']

if __name__ == "__main__":
    app.secret_key = 'oiqauwre@098QUQR234)_02349H?'
    app.run()