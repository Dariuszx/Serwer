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
            return "działa"


def GET(self, idea_id, thread_id=None):
    return NotImplemented()


class ThreadNotes:
    def GET(self, idea_id=None, thread_id=None):
        return NotImplemented()

