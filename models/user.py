from models import Model
from models.mongua import Mongua


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.user_image = 'default.png'

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None


class User(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, 'default.png'),
        ('user_address', str, ''),
        ('user_email', str, ''),
        ('user_idiograph', str, '这家伙很懒，什么个性签名都没有留下。')
    ]

    """
        User 是一个保存用户数据的 model
        现在只有两个属性 username 和 password
        """

    def __init__(self):
        self.user_image = 'default.png'

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    def user_topic(self):
        from .topic import Topic
        t = Topic.find_all(user_id=self.id)
        return t

    def topic(self):
        from .topic import Topic
        t = Topic.find_all(id=self.id)
        return t

    def reply_topic(self):
        from .reply import Reply
        t = Reply.find_all(user_id=self.id)
        return t

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.username = form.get("username", '')
        u.password = form.get("password", "")
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None

    def time(self):
        import datetime
        created_time = datetime.datetime.fromtimestamp(self.created_time)
        present_time = datetime.datetime.now()
        t = present_time - created_time

        if t.days != 0:
            return str(t.days) + '天前'
        else:
            sec = t.seconds
            if sec < 60:
                return str(sec) + '秒前'
            elif sec < 3600:
                return str(sec // 60) + '分钟前'
            else:
                return str(sec // 3600) + '小时前'
