#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import app


sys.path.insert(0, abspath(dirname(__file__)))
application = app.app

"""
建立一个软连接
ln -s /var/www/mybbs/bbs.conf /etc/supervisor/conf.d/bbs.conf

ln -s /var/www/mybbs/bbs.nginx /etc/nginx/sites-enabled/bbs

ln -s /var/www/mybbs/redis-server.conf /etc/supervisor/conf.d/redis-server.conf

ln -s /var/www/mybbs/mongod.conf /etc/supervisor/conf.d/mongod.conf



➜  ~ cat /etc/supervisor/conf.d/bbs.conf

[program:mybbs]
command=/usr/local/bin/gunicorn wsgi -c gunicorn.config.py
directory=/var/www/mybbs
autostart=true
autorestart=true


gunicorn.config.py

bind = '0.0.0.0:2001'
pid = '/tmp/bbs.pid'
"""
