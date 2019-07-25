'''
Simple Flask RESTful web service to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS
'''

from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<user>:<password>@<endpoint>:<port>/<db_name>'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(128))
    def tojson(self):
        task =  dict(t for t in self.__dict__.items() if t[0][0] != '_')
        task['uri'] = url_for('get_task', task_id=self.id, _external=True)
        return task

@application.errorhandler(500)
def error_500(error):
    return jsonify(error="Internal Server Error")

@application.errorhandler(404)
def error_404(error):
    return jsonify(error="Resource Not Found")

@application.errorhandler(400)
def error_400(error):
    return jsonify(error="Bad Request")

@application.route('/todo/api/v1.0/tasks', methods=['GET'])
def index():
    tasks = Todos.query.all()
    return jsonify([t.tojson() for t in tasks])

@application.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Todos.query.get(task_id)
        return jsonify(task.tojson())
    except:
        abort(404)

@application.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = Todos(description=request.json['description'], title=request.json['title'])
    db.session.add(task)
    db.session.commit()
    task = Todos.query.get(task.id)
    return jsonify(task.tojson()), 201

@application.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)    
    try:
        task = Todos.query.get(task_id)
        task.title = request.json.get('title', task.title)
        task.description = request.json.get('description', task.description)
        task.done = request.json.get('done', task.done)
        db.session.add(task)
        db.session.commit()
        task = Todos.query.get(task.id)
        return jsonify(task.tojson())
    except:
        abort(404)

@application.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Todos.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': True})
    except:
        abort(404)

if __name__ == '__main__':
    application.run(host='0.0.0.0')

