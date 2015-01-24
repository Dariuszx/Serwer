# encoding: utf-8
import web, json, tools

class User:

    #Tworzę nowego użytkownika
    def POST(self, user_id=None):
        dane = web.input()
        status = None

        if not dane.has_key('login') or not dane.has_key('password'): #Czy wysłano odpowiednie dane
            raise web.BadRequest()

        if len(dane.login) < 4 or len(dane.password) < 6: #Czy długość się zgadza?
            raise web.NotAcceptable()
        elif not tools.db.check_login_avavailability(dane.login): #Czy login zajęty?
            raise web.NotAcceptable()
        else: #Rejestruje użytkownika
            tools.db.register_user(dane.login, dane.password)

        user_data = tools.db.get_user_data(dane.login)

        return tools.respond({'user_id':user_data.user_id, 'login':user_data.login})

    #Edycja użytkownika
    def PUT(self):
        #TODO zmiana loginu lub hasła na podstawie danych wejściowych
        return NotImplemented()

    #Pobieram użytkownika o konkretnym id
    def GET(self, user_id = None):

        if( user_id == None ):
            raise web.NotFound()

        user = tools.db.get_user(user_id)

        print tools.respond(user)

    def DELETE(self, user_id=None):
        #TODO usuwanie użytkownika
        return NotImplemented()

#TODO dopisać
class UserNotification:

    def GET(self):
        return NotImplemented()

    def POST(self, user_id=None):
        return NotImplemented()

    def DELETE(self, user_id=None, notification_id=None):
        return NotImplemented()