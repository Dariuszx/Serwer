# encoding: utf-8
import web, json, database, tools
from web import db, HTTPError


from login import LoginManager
from user import User, UserNotification, UserIdea
from idea import Idea, IdeaFollow, IdeaMembers, IdeaThreads
from note import Note
from threads import Thread, ThreadNotes



urls = (
    '/login', 'LoginManager',                       #DONEMenadżer logowania

    '/user/idea/(.*)', 'UserIdea',
    '/user/notification/', 'UserNotification',      #TODO Operacje na notyfikacjach użytkownika
    '/user/(.*)', 'User',                           #DONEOperacje na użytkownikach
    '/note/(.*)', 'Note',                           #Operacje na notatkach

    '/idea/adduser/(.*)', 'IdeaAddUser',            #Dodawanie użytkownika do idei
    '/idea/request/(.*)', 'IdeaRequest',            #Zapytanie o dołączenie do tworzenia idei
    '/idea/follow/(.*)', 'IdeaFollow',              #Opcja śledzenia idei przez użytkownika
    '/idea/member/(.*)', 'IdeaMembers',             #Lista współtworzących ideę
    '/idea/thread/(.*)','IdeaThreads',              #Lista wątków danej idei
    '/idea/(.*)', 'Idea',                           #DONEOperacje na idei

    '/thread/note/(.*)', 'ThreadNotes',             #Notatki konkretnego wątu
    '/thread/(.*)', 'Thread',                       #DONEOperacje na konkretnym wątku
)

#Łącze się z bazą danych
mysql = web.database(dbn='mysql', user='dariusz', pw='5qnCUxyAjnY2CUpZ', db='dariusz_idea_project')

#Dzięki obiektowi tej klasy mogę operować na bazie danych
tools.db = database.Database(mysql)

class App(web.application):
    def run(self, port=8001, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0',port))


if __name__ == "__main__":
    app = App(urls, globals())
    app.internalerror = web.debugerror
    app.run(port=8001)