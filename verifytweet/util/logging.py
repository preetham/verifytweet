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

import logging
import sys

from verifytweet.config.settings import app_config

logger = logging.getLogger()
logger.setLevel(app_config.LOG_LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(app_config.LOG_LEVEL)

web_formatter = logging.Formatter(u'%(asctime)s -- %(levelname)s -- %(message)s')
cli_formatter = logging.Formatter(u'%(message)s')
formatter = cli_formatter if app_config.RUN_METHOD == "cli" else web_formatter

handler.setFormatter(formatter)
logger.addHandler(handler)
