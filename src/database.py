# encoding: utf-8
import web, hashlib
from hashlib import sha256
from os import urandom

class Database:

    db = None

    def __init__(self,db):
        self.db = db

    def check_login_avavailability(self, username):
        myvar = dict(name=username)
        entry = self.db.select('users', myvar, where="login = $name", what="1", _test=True)
        result = self.db.query(entry)

        if result:
            return False
        else:
            return True

    def register_user(self, login, password):

        salt = urandom(32).encode('base-64')
        password_encrypted = sha256(password.encode('utf-8') + "" + salt)

        q = self.db.insert('users', login=login, password=password_encrypted.hexdigest(), salt=salt)

        return None

    def get_user_data(self, login):
        myvar = dict(name=login)
        entry = self.db.select('users', myvar, what="user_id, login", where="login = $name", _test=True)
        result = self.db.query(entry)

        if not result:
            raise web.NotFound("Nie znaleziono użytkownika o podanym loginie.")
        else:
            return result[0]

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

    def get_salted_password(self, password, salt):
        password_encrypted = sha256(password.encode('utf-8') + "" + salt)
        return password_encrypted.hexdigest()
