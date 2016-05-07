from adalpython.argument import validate_string_param
import sqlite3
class Storage(object):

    def set_dbfile(self,value):
        self._dbfile = value

    def get_dbfile(self):
        return self._dbfile

    def store_state(self,state,nonce,additioninfo):
        validate_string_param(state,"State")
        self._check_database()
        connection = sqlite3.connect(self.get_dbfile())
        cursor = connection.cursor()
        query = 'INSERT INTO state(state, nonce, additional) VALUES ("{st}","{nonce}","{additional}")'.format(st=state,nonce=nonce,additional=additioninfo)
        cursor.execute(query)
        connection.commit()
        connection.close() 

    def get_state(self,state):
        validate_string_param(state,"State")
        self._check_database()
        connection = sqlite3.connect(self.get_dbfile())
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM state WHERE state='{state}'".format(state=state))
        row = cursor.fetchone()
        connection.close()
        return row[1]

    def delete_state(self,state):
        validate_string_param(state,"State")
        self._check_database()
        connection = sqlite3.connect(self.get_dbfile())
        connection.execute("DELETE FROM state WHERE state='{state}'".format(state=state))
        connection.close()

    def _check_database(self):
        connection = sqlite3.connect(self.get_dbfile())
        cursor = connection.cursor()
        cursor.execute('create table if not exists state(state TEXT, nonce TEXT, additional TEXT)')
        connection.commit()
        connection.close() 
        

