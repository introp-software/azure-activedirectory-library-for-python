import sqlite3

class App_Storage(object):
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

    def delink_user(self,db_file, user_id):        
        self.check_ad_user_table(db_file)
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('delete from ad_users where user_id = {user_id})'.format(user_id = user_id))
        connection.commit()
        connection.close()
      

