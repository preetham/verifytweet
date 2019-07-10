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

from verifytweet import controller
from verifytweet import result

non_api_approach = controller.NonAPIApproach()


def test_exec_empty_input():
    """Test exec for empty input
    """
    with pytest.raises(TypeError):
        non_api_approach.exec()


def test_exec_invalid_type_input():
    """Test exec for invalid type input
    """
    with pytest.raises(TypeError):
        non_api_approach.exec(None)
        non_api_approach.exec(123)
        non_api_approach.exec(['/home/'])


def test_exec_invalid_input():
    """Test exec for valid type invalid input
    """
    with pytest.raises(ValueError):
        non_api_approach.exec('')
    assert non_api_approach.exec(
        '123')[1] == result.ResultStatus.MODULE_FAILURE
    assert non_api_approach.exec(
        '/home')[1] == result.ResultStatus.MODULE_FAILURE
    assert non_api_approach.exec(
        'tmp.png')[1] == result.ResultStatus.MODULE_FAILURE


def test_exec_valid_input(file_path):
    """Test exec for valid input
    """
    from twint.tweet import tweet

    test_result_tweet = 'ey send me stolen pdp wave designs'
    test_result_username = 'pewdiepie'
    module_result, module_status = non_api_approach.exec(file_path)
    assert module_status == result.ResultStatus.ALL_OKAY
    assert isinstance(module_result, tweet)
    assert test_result_tweet in module_result.tweet
    assert test_result_username == module_result.username
