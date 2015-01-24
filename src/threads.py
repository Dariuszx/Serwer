# encoding: utf-8
import tools, web

class Thread:

    def POST(self, thread_id=None):
        data = web.input()

        if not data:
            raise web.BadRequest()

        if not data.has_key('user_id') or not data.has_key('idea_id') or not data.has_key('overview'):
            raise web.BadRequest()

        if not tools.db.add_thread(data.idea_id, data.user_id, data.overview):
            raise web.NotFound()
        else:
            return tools.respond(tools.status_ok)

    def GET(self, thread_id=None):
        result = tools.db.get_thread(thread_id)
        return tools.respond_database_row(result)

    def PUT(self, thread_id=None):
            data = web.input()

            if not data:
                raise web.BadRequest()
            elif not data.has_key('overview') or not data.has_key('thread_id'):
                raise web.BadRequest()
            else:
                result = tools.db.edit_thread(data)
                return tools.respond(tools.status_ok)

    #TODO zrobić usuwanie wątków
    def DELETE(self, thread_id=None):
        return tools.respond(tools.status_error)


class ThreadNotes:
    def GET(self, idea_id=None, thread_id=None):
        return NotImplemented()
