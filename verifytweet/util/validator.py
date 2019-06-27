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

import numpy

from verifytweet.config.settings import app_config
from verifytweet.util.result import ResultStatus

def verify_validity(similarity_matrix):
    """Verifies validity of a tweet in similarity matrix.

    Verifies validity of a tweet in similarity matrix, if it crosses
    the configured threshold for similarity.

    Args:
        similarity_matrix: A list of lists containing similarity scores

    Returns:
        A Boolean representing validity of the tweet.
    """
    for row in similarity_matrix:
        for column in row:
            if column > app_config.SIMILARITY_THRESHOLD:
                return (True, ResultStatus.ALL_OKAY)
    return (False, ResultStatus.ALL_OKAY)