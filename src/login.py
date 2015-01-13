# encoding: utf-8
import web, json, database


class LoginManager:

    def POST(self):
        dane = web.input()

        if not dane.login and not dane.password:
            raise web.Unauthorized()

        user_id = database.db.check_login_credentials(dane.login, dane.password)

        if user_id == -1:
            raise web.Unauthorized()
        else:
            return json.dumps({'user_id':user_id})