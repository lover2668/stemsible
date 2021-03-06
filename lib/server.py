from flask import Flask, jsonify, request

import json

from vlib import conf

from users import Users, User
from messages import Message, Messages

HTTP_BAD_REQUEST = 400

app = Flask(__name__)

@app.route('/users', methods=['GET', 'POST'])
def getUsers():
    conf_ = conf.getInstance()
    users = Users()
    if request.method == 'POST':
        data = dict((k, request.form[k]) for k in request.form.keys())
        return jsonify(users.add(data))
    else:
        users.setColumns(['id',
                          'concat_ws(" ", first_name, last_name) as fullname',
                          'created'])
        users.setOrderBy('id')
        results = users.getTable()
        data = {
            'users': [
                {'id'      : r['id'],
                 'fullname': r['fullname'],
                 'created' : r['created'],
                 'uri': 'http://%s/users/%s' % (conf_.serverurl, r['id']),
                 }
                for r in results]
            }
        return jsonify(data)

@app.route('/users/<int:id>')
def getUser(id):
    try:
        return jsonify(User(id).data)
    except Exception, e:
        return problem(e)

@app.route('/messages', methods=['GET', 'POST'])
def getMessages():
    messages = Messages()
    if request.method == 'POST':
        if request.data:
            # Content-Type: application/json
            # ie. - { "foo": "bar", "baz": "moe" }
            data = json.loads(request.data)
        else:
            # Content-Type: x-www-form-urlencoded
            # ie. - foo=bar&baz=moe
            data = dict((k, request.values[k]) for k in request.values.keys())
        return jsonify(messages.add(data))
    else:
        return jsonify(messages.getMessages())

@app.route('/messages/<int:id>')
def getMessage(id):
    try:
        message = Message(id)
        data = message.data
        data['user'] = message.user.data
        return jsonify(data)
    except Exception, e:
        return problem(e)

def problem(e):
    response = {'error': str(e)}
    return jsonify(response), HTTP_BAD_REQUEST

if __name__ == '__main__':
    app.debug = True # not for production
    app.run()
