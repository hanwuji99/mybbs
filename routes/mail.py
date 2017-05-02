from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
from models.mail import Mail


main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    mail = Mail.new(form)
    # 为了安全
    mail.set_sender(current_user().id)
    return redirect(url_for(".index"))


@main.route("/", methods=["GET"])
def index():
    u = current_user()
    send_mail = Mail.find_all(sender_id=u.id)
    received_mail = Mail.find_all(receiver_id=u.id)

    return render_template("mail/mail_index.html", user=u, sends=send_mail, receives=received_mail)


@main.route("/view/<int:id>")
def view(id):
    mail = Mail.find(id)
    # 不是你自己发的，你肯定不能看
    # 不是收的人，那你看了也不会变成已读
    if current_user().id == mail.receiver_id:
        mail.mark_read()
    if current_user().id in [mail.receiver_id, mail.sender_id]:
        return render_template("mail/mail_detail.html", mail=mail)
    else:
        return redirect(url_for(".index"))

