import sqlite3
from user import User
class storage(object):
    """description of class"""
    def check_user_table(self, db_file):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('create table if not exists users(id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, password TEXT, email TEXT)')
        connection.commit()
        connection.close()

    def check_user(self,db_file,username,password):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('select email, password, firstname, lastname, id from users where email = "{username}"'.format(username=username))
        row = cursor.fetchone()
        connection.close()
        if row is None:
            return "User does not exist"
        if row[1] != password:
            return "Password does not match"
        user = User()
        user.FirstName = row[2]
        user.LastName = row[3]
        user.Email = username
        user.Id = row[4]
        return user

    def create_user(self,db_file,user):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('insert into users(firstname, lastname, password, email) VALUES ("{firstname}","{lastname}","{password}","{email}")'.
                       format(firstname = user.FirstName, lastname= user.LastName, password = user.Password, email = user.Email))
        connection.commit()
        connection.close()

      

