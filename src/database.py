# encoding: utf-8
import web, hashlib
from hashlib import sha256
from os import urandom

class Database:

    db = None

    def __init__(self,db):
        self.db = db

    #CHECKS
    def check_login_avavailability(self, username):
        myvar = dict(name=username)
        entry = self.db.select('users', myvar, where="login = $name", what="1", _test=True)
        result = self.db.query(entry)

        if result:
            return False
        else:
            return True

    def check_login_credentials(self, login, password):

        password_db = None
        salt_db = None
        userid_db = None
        myvar = dict(name=login)
        entry = self.db.select('users', myvar, what="user_id, password, salt", where="login = $name")

        if entry:
            for row in entry:
                userid_db = row.user_id
                password_db = row.password
                salt_db = row.salt

            encrypted_password = self.get_salted_password(password, salt_db)

            if encrypted_password != password_db:
                return -1
            else:
                return userid_db

    def check_user_id(self, user_id):
        query = "SELECT 1 FROM users WHERE user_id="+user_id
        result = self.db.query(query)

        if not result:
            return False
        else:
            return True

    def check_idea_id(self, idea_id):

        query = "SELECT 1 FROM idea WHERE idea_id=" + idea_id
        result = self.db.query(query)

        if not result:
            return False
        else:
            return True

    def register_user(self, login, password):

        salt = urandom(32).encode('base-64')
        password_encrypted = sha256(password.encode('utf-8') + "" + salt)


        q = self.db.insert('users', login=login, password=password_encrypted.hexdigest(), salt=salt, _test = True)
        self.db.query(q)

        return None

    #GETS
    def get_user_data(self, login):
        myvar = dict(name=login)
        entry = self.db.select('users', myvar, what="user_id, login", where="login = $name", _test=True)
        result = self.db.query(entry)

        if not result:
            raise web.NotFound("Nie znaleziono użytkownika o podanym loginie.")
        else:
            return result[0]

    def get_user(self, user_id):

        myvar = dict(id=user_id)
        entry = self.db.select('users', myvar, what="user_id, login", where="user_id = $id", _test=True)
        result = self.db.query(entry)

        if not result:
            raise web.NotFound("Nie znaleziono użytkownika o podanym user_id.")
        else:
            return result[0]

    def get_idea(self, idea_id):
        query = "SELECT idea.title, idea.date, users.user_id, users.login FROM idea INNER JOIN users \
ON idea.user_id = users.user_id WHERE idea.idea_id="+idea_id

        result = self.db.query(query)

        if not result:
            raise web.NotFound("Nie ma takiej idei")
        else:
            return result[0]

    #ADDS
    def add_idea(self, user_id, title, right_id=None, background_image=None):
    #TODO dopisać obsługe wczytywania do bazy danych obrazków tła i praw widoczności
        if not self.check_user_id(user_id):
            raise web.NotAcceptable("Użytkownik o podanym id nie istnieje")
        else:
            query = self.db.insert('idea', user_id=user_id, right_id=1, title=title)
            #self.db.query(query)

    #EDITS
    def edit_idea(self, idea_id, data):

        what = ""

        for key, value in data.iteritems():
            v = value.encode('utf-8')
            what += key + "=\"" + v + "\" "

        query = "UPDATE idea SET " + what.decode('utf-8') + "WHERE idea_id=" + idea_id

        self.db.query(query)

    def get_salted_password(self, password, salt):
        password_encrypted = sha256(password.encode('utf-8') + "" + salt)
        return password_encrypted.hexdigest()
