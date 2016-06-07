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
import sqlite3

class app_storage(object):
    def check_user_table(self, db_file):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('create table if not exists users(id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, password TEXT, email TEXT)')
        connection.commit()
        connection.close()

    def check_ad_user_table(self,db_file):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('create table if not exists ad_users(id INTEGER PRIMARY KEY, user_id INTEGER, token TEXT, token_type TEXT, o365_email TEXT)')
        connection.commit()
        connection.close()

    def login_user(self,db_file,username,password):
        self.check_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('select email, password, firstname, lastname, id from users where email = "{username}"'.format(username=username))
        row = cursor.fetchone()
        connection.close()
        if row is None:
            raise ValueError("User does not exist")
        if row[1] != password:
            raise ValueError("Password does not match") 
        return row

    def create_user(self,db_file,user):
        self.check_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('insert into users(firstname, lastname, password, email) VALUES ("{firstname}","{lastname}","{password}","{email}")'.
                       format(firstname = user.FirstName, lastname= user.LastName, password = user.Password, email = user.Email))
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return user_id

    def get_ad_user(self,db_file,userid):
        self.check_ad_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('select id, o365_email from ad_users where user_id = "{user_id}"'.format(user_id=userid))
        row = cursor.fetchone()
        connection.close()
        if row is None:
            raise LookupError("This user is not linked")
        return row[1]

    def get_ad_user_by_email(self,db_file,email):
        self.check_ad_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('select id, o365_email,token,token_type from ad_users where o365_email = "{email}"'.format(email=email))
        row = cursor.fetchone()
        connection.close()
        if row is None:
            raise LookupError("User does not exist")
        return row

    def get_user_by_email(self,db_file,email):
        self.check_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('select email, password, firstname, lastname, id from users where email = "{username}"'.format(username=email))
        row = cursor.fetchone()
        connection.close()
        if row is None:
            raise LookupError("This user is not registered")
        return row

    def link_user(self,db_file, user_id,ad_user):
        self.check_user_table(db_file)
        self.check_ad_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('insert into ad_users(user_id, token, token_type, o365_email) VALUES ("{user_id}","{token}","{token_type}","{o365_email}")'.
                       format(user_id = user_id, token= ad_user.Token, token_type = '', o365_email = ad_user.O365_Email))
        connection.commit()
        connection.close()

    def create_ad_user(self,db_file,ad_user):
        self.check_ad_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('insert into ad_users( token, token_type, o365_email) VALUES ("{token}","{token_type}","{o365_email}")'.
                       format(token= ad_user.Token, token_type = 'token', o365_email = ad_user.O365_Email))
        connection.commit()
        connection.close()

    def update_ad_user(self,db_file,ad_user):
        self.check_ad_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('update ad_users set token = "{token}" where o365_email = "{o365_email}"'.
                       format(token= ad_user.Token, o365_email = ad_user.O365_Email))
        connection.commit()
        connection.close()

    def delink_user(self,db_file, email): 
        try:       
            self.check_ad_user_table(db_file)
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()
            cursor.execute('delete from ad_users where o365_email = "{o365email}"'.format(o365email = email))
            connection.commit()
            connection.close()
        except Exception as ex:
            raise Exception(ex)
      

