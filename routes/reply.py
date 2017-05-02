from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.reply import Reply


main = Blueprint('reply', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Reply.new(form, user_id=u.id)
    from .topic import Topic
    t = Topic.find_by(id=m.topic_id)
    t.last_time = m.created_time
    t.save()
    return redirect(url_for('topic.detail', id=m.topic_id))

