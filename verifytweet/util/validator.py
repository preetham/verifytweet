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

from numpy import ndarray

from verifytweet.config.settings import app_config
from verifytweet.util.result import ResultStatus

def verify_validity(similarity_matrix: ndarray):
    """Verifies validity of a tweet in similarity matrix.

    Verifies validity of a tweet in similarity matrix, if it crosses
    the configured threshold for similarity.

    Args:
        similarity_matrix: A list of lists containing similarity scores

    Returns:
        A Boolean representing validity of the tweet.
    """
    if not isinstance(similarity_matrix, ndarray):
        raise TypeError('Similarity matrix must type numpy.ndarray')
    row = similarity_matrix[0]
    for column_index in range(1, row.shape[0]):
        if row[column_index] > app_config.SIMILARITY_THRESHOLD:
            return (True, column_index, ResultStatus.ALL_OKAY)
    return (False, None, ResultStatus.ALL_OKAY)
