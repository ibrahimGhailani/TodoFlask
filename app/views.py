from app import app, models, db
import flask


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/task', methods=['POST'])
def add_task():
    try:
        task_json = flask.request.get_json()
        if "title" not in task_json or "content" not in task_json:
            flask.abort(400)
        else:
            # TODO: get user from token
            u = models.User.query.filter_by(username="ibrahim").first()
            t = models.Task(title=task_json.get("title"),
                            content=task_json.get("content"),
                            user=u)
            db.session.add(t)
            db.session.commit()
            return flask.jsonify(t.to_dict()), 201
    except Exception:
        flask.abort(400)


@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task_json = flask.request.get_json()

        # TODO: get user from token
        u = models.User.query.filter_by(username="ibrahim").first()
        t = models.Task.query.filter_by(id=task_id, user_id=u.id).first()
        if t is not None:
            if "title" in task_json:
                t.title = task_json.get("title")
            if "content" in task_json:
                t.content = task_json.get("content")
            if "done" in task_json:
                print task_json
                t.done = task_json.get("done")
            db.session.commit()
            return flask.jsonify(t.to_dict()), 200
        else:
            return not_found("Not found")
    except Exception, e:
        print e.message
        flask.abort(400)


@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        # TODO: get user from token
        u = models.User.query.filter_by(username="ibrahim").first()
        t = models.Task.query.filter_by(id=task_id, user_id=u.id).first()
        if t is not None:
            db.session.delete(t)
            db.session.commit()
            return flask.jsonify({"message": "Task removed"}), 200
        else:
            return not_found()
    except Exception, e:
        print e.message
        flask.abort(400)


@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    result = models.Task.query.filter_by(id=task_id).first()
    if result is not None:
        return flask.jsonify(result.to_dict())
    else:
        flask.abort(404)


@app.route("/task", methods=['GET'])
def get_tasks():
    results = []
    tasks = models.Task.query.all()

    for task in tasks:
        results.append(task.to_dict())

    return flask.jsonify({"tasks": results})


def create_user():
    return


@app.errorhandler(404)
def not_found(error="Not found"):
    return flask.jsonify({"message": error}), 404


@app.errorhandler(401)
def unauthorized(error="Unauthorized"):
    return flask.jsonify({"message": error}), 401


@app.errorhandler(400)
def bad_request(error="Bad request"):
    return flask.jsonify({"message": error}), 400
