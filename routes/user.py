from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
from models.user import User
from models.topic import Topic
from models.mail import Mail


main = Blueprint('user', __name__)


@main.route("/<username>")
def user(username):
    u = current_user()
    user = User.find_by(username=username)
    t = user.user_topic()

    topics = user.reply_topic()
    a = []
    test = []
    for topic in topics:
        if topic.topic_id not in test:
            test.append(topic.topic_id)
            a.append(Topic.find_all(id=topic.topic_id))
    return render_template("user/user_detail.html", username=username, user_slide=u, user=user, ms=t, a=a)


@main.route("/<username>/mail")
def mail(username):
    u = current_user()
    user = User.find_by(username=username)
    return render_template("mail/send_mail.html", username=username, receiver_user=user)


@main.route("/mail_add", methods=["POST"])
def mail_add():
    form = request.form
    mail = Mail.new(form)
    # 为了安全
    mail.set_sender(current_user().id)
    return redirect(url_for("mail.index"))
