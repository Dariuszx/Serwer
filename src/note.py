# encoding: utf-8
import tools, web, json

class Note:

    def GET(self, note_id=None):
        result = tools.db.get_note(note_id)
        return tools.respond_database_row(result)

    def POST(self, note_id=None):
        data = web.input()

        print data

        if not data.has_key('user_id') or not data.has_key('thread_id') or not data.has_key('content'):
            raise web.BadRequest()

        if not tools.db.add_note(data.user_id, data.thread_id, data.content):
            raise web.BadRequest()

    def PUT(self, note_id=None):
        data = web.input()

        if not data.has_key("note_id") or not data.has_key("content"):
            raise web.BadRequest()

        tools.db.edit_note(data.note_id, data.content)

    def DELETE(self, note_id=None):
        tools.db.delete_note(note_id)


