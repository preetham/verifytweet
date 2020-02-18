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

import pytest
import numpy

from verifytweet import validator
from verifytweet import settings
from verifytweet import result

app_config = settings.app_config
app_config.SIMILARITY_THRESHOLD = 0.6

def test_validator_empty_input():
    """Test verify validity for empty input
    """
    with pytest.raises(TypeError):
        validator.verify_validity()


def test_validator_invalid_type_input():
    """Test verify validity for invalid type input
    """
    with pytest.raises(TypeError):
        validator.verify_validity(None)
        validator.verify_validity(list())
        validator.verify_validity([[]])


def test_validator_valid_similarity_matrix():
    """Test verfiy validity for valid similarity matrix
    """
    test_numpy_array = numpy.array([[1., 0.7, 0.6], [0.5, 0.1, 1.]])
    module_result, match_index, result_status = validator.verify_validity(test_numpy_array)
    assert result_status == result.ResultStatus.ALL_OKAY
    assert module_result == True


def test_validator_invalid_similarity_matrix():
    """Test verfiy validity for valid similarity matrix
    """
    test_numpy_array = numpy.array([[0.1, 0.1], [0.1, 0.1]])
    module_result, match_index, result_status = validator.verify_validity(test_numpy_array)
    assert result_status == result.ResultStatus.ALL_OKAY
    assert module_result == False
