# encoding: utf-8
import tools, web, json

class Note:

    def GET(self, user_id, note_id=None):
        return NotImplemented()

    def POST(self, note_id=None):
        data = web.input()

        print data

        if not data.has_key('user_id') or not data.has_key('thread_id') or not data.has_key('content'):
            raise web.BadRequest()

        if not tools.db.add_note(data.user_id, data.thread_id, data.content):
            raise web.BadRequest()


    def PUT(self, note_id=None):
        return NotImplemented()

    def DELETE(self, note_id=None):
        return NotImplemented()
