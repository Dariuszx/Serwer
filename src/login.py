# encoding: utf-8
import web, json, database, tools


class LoginManager:

    #Loguje się do systemu
    def POST(self):
        dane = web.input()

        if not dane.has_key('login') and not dane.has_key('password'):
            raise web.Unauthorized()

        user_id = tools.db.check_login_credentials(dane.login, dane.password)

        if not user_id or user_id == -1:
            raise web.Unauthorized()
        else:
            return tools.respond({'user_id':user_id})