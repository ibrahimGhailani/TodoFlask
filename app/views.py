from app import app, models
import flask


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/task', methods=['POST'])
def add_task():
    return


@app.route('/task', methods=['UPDATE'])
def mark_task_as_done():
    return


@app.route('/task', methods=['DELETE'])
def delete_task():
    return


@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    result = models.Task.query.filter_by(id=task_id).first()
    if result is not None:
        return flask.jsonify(result.to_dict())
    else:
        return flask.jsonify({})


@app.route("/task", methods=['GET'])
def get_tasks():
    results = []
    tasks = models.Task.query.all()

    for task in tasks:
        results.append(task.to_dict())

    return flask.jsonify({"tasks": results})


def create_user():
    return
