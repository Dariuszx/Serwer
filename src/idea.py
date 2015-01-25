# encoding: utf-8
import tools, web, json


class Idea:

    #Pobieram informacje o konkretnej idei
    def GET(self, idea_id=None):
        idea = tools.db.get_idea(idea_id)
        return tools.respond_database_row(idea)

    #Tworzenie nowej idei
    def POST(self, idea_id=None):
        #TODO dopisać wczytywanie obrazków ŧła i nadawania praw
        data = web.input()

        if not data.has_key('user_id') or not data.has_key('title'):
            raise web.BadRequest("Nie podano wystarczających danych")
        else:
            tools.db.add_idea(data.user_id, data.title)
            return tools.respond(tools.status_ok)

    #Aktualizacja konkretnej idei
    def PUT(self, idea_id=None):
        data = web.input()

        if not data:
            raise web.BadRequest("Niepoprawne dane do zmienienia")
        elif not tools.db.check_idea_id(idea_id):
            raise web.NotFound()
        else:
            if not data.has_key('title') and not data.has_key('background_image') and not data.has_key('right_id'):
                raise web.BadRequest("Nie podano danych do zmiany")
            else:
                tools.db.edit_idea(idea_id, data)
                return tools.respond(tools.status_ok)

    #Usuwanie konkretnej idei
    def DELETE(self, idea_id=None):
        if not tools.db.delete_idea(idea_id):
            raise web.NotFound()
        else:
            return "działa"

class IdeaMembers:

    def GET(self, idea_id):
        return NotImplemented()

class IdeaFollow:

    def POST(self, idea_id):
        return NotImplemented()

class IdeaThreads:

    def GET(self, idea_id=None):
        result = tools.db.get_thread(None, idea_id)
        return tools.respond_database_row(result)



class IdeaRequest:

    def POST(self):
        return NotImplemented()

class IdeaAdduser:

    def POST(self):
        return NotImplemented()