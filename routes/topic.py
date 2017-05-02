from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    send_from_directory,
    abort,
)

from routes import *

from models.topic import Topic
from models.board import Board

from utils import allow_file
from models.user import User
from werkzeug.utils import secure_filename
from config import user_file_director
import os
import uuid


main = Blueprint('topic', __name__)

csrf_tokens = dict()


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


# Topic
@main.route("/")
def index():
    # board_id = 2
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        # ms = Topic.all()
        ms = Topic.cache_all()
        # ms = Topic.all_delay()
    else:
        ms = Topic.find_all(board_id=board_id)
        # ms = Topic.cache_find(board_id)
    token = str(uuid.uuid4())
    u = current_user()
    if u is None:
        return redirect(url_for('.signin'))
    else:
        csrf_tokens['token'] = u.id
        bs = Board.all()
        return render_template("topic/index.html", user=u, ms=ms, token=token, bs=bs)


@main.route('/topic/<int:id>')
def detail(id):
    u = current_user()
    m = Topic.get(id)
    other_topic = m.other_topic()

    return render_template("topic/detail.html", user=u, topic=m, other_topic=other_topic)


@main.route("/topic/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/topic/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    # 判断 token 是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            print('删除 topic 用户是', u, id)
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/topic/new")
def new():
    u = current_user()
    bs = Board.all()
    return render_template("topic/new.html", user=u, bs=bs)


# login
@main.route("/signin")
def signin():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.signin'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('.signin'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('.index'))


@main.route("/key_login", methods=['POST'])
def key_login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


# setting
@main.route('/setting')
def setting():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


@main.route('/setting/user', methods=['POST'])
def setting_user():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        u.update(request.form)
        return redirect(url_for(".setting"))


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for(".setting"))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for(".setting"))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)


@main.route("/logout")
def log_out():
    session.pop("user_id")
    return redirect(url_for(".index"))
