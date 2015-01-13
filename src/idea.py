# encoding: utf-8


class Idea:

    def GET(self, idea_id=None):
        return NotImplemented()

class IdeaMembers:

    def GET(self, idea_id):
        return NotImplemented()

class IdeaFollow:

    def POST(self, idea_id):
        return NotImplemented()

class IdeaThreads:

    def GET(self, user_id, note_id=None):
        return NotImplemented()

class IdeaRequest:

    def POST(self):
        return NotImplemented()

class IdeaAdduser:

    def POST(self):
        return NotImplemented()