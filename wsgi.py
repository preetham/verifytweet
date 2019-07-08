# Verify Tweet verifies tweets of a public user
# from tweet screenshots: real or generated from
# tweet generators.
# Copyright (C) 2019 Preetham Kamidi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import os
import traceback

import gunicorn.app.base
from gunicorn.six import iteritems

os.environ["VERIFYTWEET_RUN_FOR_WEB"] = "true"

from verifytweet.config.settings import app_config
from verifytweet.app import router


class VerifyTweetApp(gunicorn.app.base.BaseApplication):
    """Serves Verify Tweet app using Gunicorn.

    Serves Verify Tweet app over http using Gunicorn's
    BaseApplication class.

    Attributes:
        app: Flask app which needs to be served.
        options: Gunicorn configuration dictionary
    """

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
    VerifyTweetApp(router, options).run()
