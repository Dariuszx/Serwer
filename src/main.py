# encoding: utf-8
import web, json, database, tools
from web import db, HTTPError


from login import LoginManager
from user import User, UserNotification
from idea import Idea, IdeaFollow, IdeaMembers
from note import Note
from threads import Thread, ThreadNotes



urls = (
    '/login', 'LoginManager',                       #Menadżer logowania

    '/user/notification/', 'UserNotification',#Operacje na notyfikacjach użytkownika
    '/user/(.*)', 'User',                           #Operacje na użytkownikach

    '/note/(.*)', 'Note',                           #Operacje na notatkach
    '/idea/(.+)/add/user/(.+)', 'IdeaAddUser',      #Dodawanie użytkownika do idei
    '/idea/(.+)/request', 'IdeaRequest',            #Zapytanie o dołączenie do tworzenia idei
    '/idea/(.+)/follow', 'IdeaFollow',              #Opcja śledzenia idei przez użytkownika
    '/idea/(.+)/member', 'IdeaMembers',             #Lista współtworzących ideę
    '/idea/(.+)/thread','IdeaThreads',              #Lista wątków danej idei
    '/idea/(.*)', 'Idea',                           #Operacje na idei

    '/thread/(.+)/note', 'ThreadNotes',             #Notatki konkretnego wątu
    '/thread/(.*)', 'Thread',                       #Operacje na konkretnym wątku
)

#Łącze się z bazą danych
mysql = web.database(dbn='mysql', user='dariusz', pw='***', db='dariusz_idea_project')

#Dzięki obiektowi tej klasy mogę operować na bazie danych
tools.db = database.Database(mysql)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()