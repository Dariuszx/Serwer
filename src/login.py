# encoding: utf-8
import web, json, database, tools


class LoginManager:

    def POST(self):
        dane = web.input()

        if not dane.login and not dane.password:
            raise web.Unauthorized()

        user_id = tools.db.check_login_credentials(dane.login, dane.password)

        if user_id == -1:
            raise web.Unauthorized()
        else:
            tools.add_token(user_id)
            return json.dumps({'user_id':user_id, 'token':tools.get_token(user_id)})