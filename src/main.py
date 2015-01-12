# encoding: utf-8
import web, json
from web import db, HTTPError
from database import Database


urls = (
    '/login', 'LoginManager',                       #Menadżer logowania

    '/user/(.+)/notifications', 'UserNotifications',#Operacje na notyfikacjach użytkownika
    '/user/(.*)', 'User',                           #Operacje na użytkownikach

    '/note/(.*)', 'Note',                           #Operacje na notatkach

    '/idea/(.+)/add/user/(.+)', 'IdeaAddUser',      #Dodawanie użytkownika do idei
    '/idea/(.+)/request', 'IdeaRequest',            #Zapytanie o dołączenie do tworzenia idei
    '/idea/(.+)/follow', 'IdeaFollow',              #Opcja śledzenia idei przez użytkownika
    '/idea/(.+)/member', 'IdeaMembers',             #Lista współtworzących ideę
    '/idea/(.+)/thread','IdeaThreads',              #Lista wątków danej idei
    '/idea/(.*)', 'Idea',                           #Informacje o idei

    '/thread/(.+)/note', 'ThreadNotes',             #Notatki konkretnego wątu
    '/thread/(.*)', 'Thread',                       #Operacje na konkretnym wątku
)

#Łącze się z bazą danych
db = web.database(dbn='mysql', user='dariusz', pw='***', db='dariusz_idea_project')

#Dzięki obiektowi tej klasy mogę operować na bazie danych
database = Database(db)


class LoginManager:

    def POST(self):
        dane = web.input()

        if not dane.login and not dane.password:
            raise web.Unauthorized()

        user_id = database.check_login_credentials(dane.login, dane.password)

        if user_id == -1:
            raise web.Unauthorized()
        else:
            return json.dumps({'user_id':user_id})

class User:

    def POST(self):
        dane = web.input()
        status = None

        if dane.login and dane.password: #Czy wysłano odpowiednie dane
            if len(dane.login) < 4 or len(dane.password) < 6: #Czy długość się zgadza?
                raise web.NotAcceptable()
            elif not database.check_login_avavailability(dane.login): #Czy login zajęty?
                raise web.NotAcceptable()
            else: #Rejestruje użytkownika
                database.register_user(dane.login, dane.password)

        user_data = database.get_user_data(dane.login)

        return json.dumps({'user_id':user_data.user_id, 'login':user_data.login})

    def PUT(self):
        return NotImplemented()

    def GET(self, user_id=None):
        return "usder"

    def DELETE(self, user_id=None):
        return NotImplemented()

class Note:

    def GET(self, user_id, note_id=None):
        return "dziala"

    def POST(self):
        return NotImplemented()

    def PUT(self, note_id=None):
        return NotImplemented()

    def DELETE(self, note_id=None):
        return NotImplemented()

class Thread:

    def GET(self, idea_id, thread_id=None):
        return "thread"

class ThreadNotes:

    def GET(self, idea_id=None, thread_id=None):
        return idea_id + " " + thread_id

class Idea:

    def GET(self, idea_id=None):
        return "Idea"

class IdeaMembers:

    def GET(self, idea_id):
        return "ideaMembers"

class IdeaFollow:

    def POST(self, idea_id):
        return "IdeaFollow"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()