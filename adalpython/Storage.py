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

from adalpython.argument import validate_string_param
import sqlite3
class Storage(object):

    def __init__(self, **kwargs):
       self._dbfile = None

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
        

