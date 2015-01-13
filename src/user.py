# encoding: utf-8
import web, json


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
        return user_id

    def DELETE(self, user_id=None):
        return NotImplemented()


class UserNotification:

    def GET(self, user_id=None):
        return NotImplemented()

    def POST(self, user_id=None):
        return NotImplemented()

    def DELETE(self, user_id=None, notification_id=None):
        return NotImplemented()