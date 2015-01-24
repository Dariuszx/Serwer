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

        if not user_id.isdigit():
            return False

        query = "SELECT 1 FROM users WHERE user_id="+user_id
        result = self.db.query(query)

        if len(result) == 0:
            return False
        else:
            return True

    def check_idea_id(self, idea_id):

        if not idea_id.isdigit():
            return False

        query = "SELECT 1 FROM idea WHERE idea_id=" + idea_id
        result = self.db.query(query)

        if len(result) == 0:
            return False
        else:
            return True

    def register_user(self, login, password):

        salt = urandom(32).encode('base-64')
        password_encrypted = sha256(password.encode('utf-8') + "" + salt)


        q = self.db.insert('users', login=login, password=password_encrypted.hexdigest(), salt=salt, _test = True)
        self.db.query(q)

        return None

    def check_thread_id(self, thread_id):
        if thread_id == None:
            return False
        elif not thread_id.isdigit():
            return False

        query = "SELECT 1 FROM idea_threads WHERE thread_id=" + thread_id
        result = self.db.query(query)

        if len(result) == 0:
            return False
        else:
            return True

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

        where = ""

        if idea_id:
            where = "WHERE idea.idea_id="+idea_id

        query = "SELECT idea.title, idea.date, users.user_id, users.login FROM idea INNER JOIN users \
ON idea.user_id = users.user_id " + where + " LIMIT 10"

        result = self.db.query(query)

        if not result:
            raise web.NotFound("Nie ma takiej idei")
        else:
            return result

    def get_thread(self, thread_id = None, idea_id = None):

        query_beginning = "SELECT * FROM idea_threads "
        query_end = ""

        if thread_id != None and not self.check_thread_id(thread_id):
            raise web.NotFound()
        elif idea_id != None and not self.check_idea_id(idea_id):
            raise web.NotFound()
        elif idea_id != None:
            query_end = "WHERE idea_id=" + idea_id
        elif thread_id != None:
            query_end = "WHERE thread_id=" + thread_id

        query = query_beginning + query_end

        result = self.db.query(query)
        return result

    def get_salted_password(self, password, salt):
        password_encrypted = sha256(password.encode('utf-8') + "" + salt)
        return password_encrypted.hexdigest()

    #ADDS
    def add_idea(self, user_id, title, right_id=None, background_image=None):
    #TODO dopisać obsługe wczytywania do bazy danych obrazków tła i praw widoczności
        if not self.check_user_id(user_id):
            raise web.NotAcceptable("Użytkownik o podanym id nie istnieje")
        else:
            query = self.db.insert('idea', user_id=user_id, right_id=1, title=title)
            #self.db.query(query)

    def add_thread(self, idea_id, user_id, overview):
        if not self.check_idea_id(idea_id) or not self.check_user_id(user_id):
            raise web.NotFound()

        #TODO warunek na to czy dany user_id może dodać wątek w idei
        if not True:
            raise web.Unauthorized()

        query = "INSERT INTO idea_threads (idea_id, overview) VALUES (" + idea_id + ", \"" + overview + "\")";
        if self.db.query(query) == 0:
            return False
        else:
            return True

    #EDITS
    def edit_idea(self, data):

        what = ""

        for key, value in data.iteritems():
            v = value.encode('utf-8')
            what += key + "=\"" + v + "\" "

        query = "UPDATE idea SET " + what.decode('utf-8') + "WHERE idea_id=" + idea_id

        self.db.query(query)

    def edit_thread(self, data):
        if not self.check_thread_id(data.thread_id):
            raise web.NotFound()
        else:
            query = "UPDATE idea_threads SET overview=\"" + data.overview + "\" WHERE thread_id=" + data.thread_id

            result = self.db.query(query)


    #DELETE
    def delete_idea(self, idea_id):

        if not self.check_idea_id(idea_id):
            return False
        else:
            query = "DELETE FROM idea WHERE idea_id=" + idea_id
            self.db.query(query)
            return True