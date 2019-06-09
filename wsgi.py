from __future__ import unicode_literals

import os
import traceback

import gunicorn.app.base
from gunicorn.six import iteritems

from app.router import app_router
from app.config.config import app_config



class VerifyTweetApp(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(VerifyTweetApp, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % (app_config.APP_HOST, app_config.APP_PORT),
        'workers': app_config.WORKER_COUNT,
        'timeout': app_config.TIMEOUT,
        'worker_class': app_config.WORKER_CLASS
    }
    VerifyTweetApp(app_router, options).run()
