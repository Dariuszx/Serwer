# encoding: utf-8

import calendar, time, web, json, json_utils
from os import urandom
from bson import json_util

db = None
status_ok = {'Status':200}
status_error = {'Status':400}

class Token:

    createdTime = None
    expirationTime = None
    token = None
    user_id = None

    def __init__(self, expiration, user_id):
        self.createdTime = calendar.timegm(time.gmtime())
        self.expirationTime = self.createdTime + expiration
        self.token = make_token()
        self.user_id = user_id

    def check_validity(self):
        if self.expirationTime <= calendar.timegm(time.gmtime()):
            return False
        else:
            return True

tokens = {}


def respond_database_row(rows):
    json_row = []
    for v in rows:
        json_row.append(v)
    return respond(json_row)


def respond(data):
    web.header('Content-Type', 'application/json')
    return json.dumps(data, default=json_util.default)

def make_token():
    return urandom(32).encode('base-64')

def add_token(user_id):

    if not user_id in tokens:
        tokens[user_id] = Token(1800, user_id)

def remove_token(user_id, token):
    if user_id in tokens and tokens.get(user_id).token == token:
        print "usuwam"
        tokens.pop(user_id)

def check_token(user_id, tk):

    token = tokens.get(user_id)

    if token.check_validity():
        return True
    else:
        return False

def get_token(user_id):
    if user_id in tokens:
        return tokens[user_id]
    else:
        return None
