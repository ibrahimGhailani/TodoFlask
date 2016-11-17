import os, uuid

from app import app, models, db, auth
from flask import (request, jsonify, abort, g, send_from_directory)
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


'''
    Task CRUD
'''


@app.route('/task/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    try:
        task_json = request.get_json()

        t = models.Task.query.filter_by(id=task_id, user_id=g.user.id).first()
        if t is not None:
            if "title" in task_json:
                t.title = task_json.get("title")
            if "content" in task_json:
                t.content = task_json.get("content")
            if "done" in task_json:
                print task_json
                t.done = task_json.get("done")
            db.session.commit()
            return jsonify(t.to_dict()), 200
        else:
            return bad_request("Task Not Found", 4004)
    except Exception, e:
        print e.message
        abort(400)


@app.route('/task', methods=['POST'])
@auth.login_required
def add_task():
    try:
        task_json = request.get_json()
        if "title" not in task_json or "content" not in task_json:
            return bad_request()
        else:
            t = models.Task(title=task_json.get("title"),
                            content=task_json.get("content"),
                            user=g.user)
            db.session.add(t)
            db.session.commit()
            return jsonify(t.to_dict()), 201
    except Exception:
        return bad_request()


@app.route('/task/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    try:
        t = models.Task.query.filter_by(id=task_id, user_id=g.user.id).first()
        if t is not None:
            db.session.delete(t)
            db.session.commit()
            return jsonify({"message": "Task removed"}), 200
        else:
            return bad_request("Task Not Found", 4004)
    except Exception:
        return bad_request()


@app.route('/task/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    result = models.Task.query.filter_by(id=task_id).first()
    if result is not None:
        return jsonify(result.to_dict())
    else:
        return bad_request("Task not found", 4004)


@app.route("/task", methods=['GET'])
@auth.login_required
def get_tasks():
    results = []
    tasks = models.Task.query.filter_by(user_id=g.user.id)
    for task in tasks:
        results.append(task.to_dict())

    return jsonify({"tasks": results})


'''
    Upload Images
'''


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_IMAGE_EXTENSION']


@app.route("/upload/<upload_id>", methods=['POST'])
@auth.login_required
def upload_image(upload_id):
    if 'file' not in request.files:
        return bad_request("No file part")
    image_file = request.files['file']
    if image_file.filename == '':
        return bad_request('No selected file')
    image = models.Image.query.filter_by(id=upload_id).first()
    if image is None:
        return bad_request('id not found')
    if image_file and allowed_extension(image_file.filename):
        filename = secure_filename(image_file.filename)
        filename = str(uuid.uuid4()) + "." + filename.rsplit('.', 1)[1]
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image.url = filename
        db.session.commit()
        return jsonify(image.to_dict()), 200
    else:
        print "Extension not allowed"
        return bad_request()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/upload', methods=["POST"])
def update_image_information():
    json = request.get_json()
    if 'caption' in json and 'task_id' in json:
        image = models.Image(caption=json.get('caption'), task_id=json.get('task_id'))
        db.session.add(image)
        db.session.commit()
        return jsonify(image.to_dict()), 201
    else:
        return bad_request("missing parameters", 4002)


'''
    Create new user
'''


@app.route("/user", methods=["POST"])
def create_user():
    user_json = request.get_json()
    if "username" in user_json and "email" in user_json and "password" in user_json:
        if models.User.query.filter_by(username=user_json.get("username")).first() is None:
            if models.User.query.filter_by(email=user_json.get("email")).first() is None:
                u = models.User(username=user_json.get("username"),
                                email=user_json.get("email"))
                u.hash_password(user_json.get("password"))
                db.session.add(u)
                db.session.commit()
                return jsonify(u.to_dict()), 201
            else:
                return bad_request("Email exists", 4003)
        else:
            return bad_request("Username exists", 4001)
    else:
        return bad_request()


'''
    Auth
'''


@app.route('/login')
@auth.login_required
def login():
    return jsonify({'login': True})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = models.User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/user", methods=["GET"])
@auth.login_required
def get_users():
    users = models.User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


'''
    Error Handling
'''


@app.errorhandler(404)
def not_found(error="", code=404):
    return jsonify({"message": "Not found", "code": code}), 404


@app.errorhandler(401)
@auth.error_handler
def unauthorized(error="", code=401):
    return jsonify({"message": "Unauthorized access", "code": code}), 401


@app.errorhandler(400)
def bad_request(msg="Bad request", code=400):
    return jsonify({"message": msg, "code": code}), 400
