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

from verifytweet import common
from verifytweet import result

def test_extract_and_parse_empty_input():
    """Test extract_and_parse for empty input
    """
    with pytest.raises(TypeError):
        common.extract_and_parse()


def test_extract_and_parse_invalid_type_input():
    """Test extract_and_parse for invalid input type
    """
    with pytest.raises(TypeError):
        common.extract_and_parse(1234)
        common.extract_and_parse(None)


def test_extract_and_parse_invalid_input():
    """Test extract_and_parse for invalid file path
    """
    with pytest.raises(ValueError):
        common.extract_and_parse('')
    module_result, result_status = common.extract_and_parse('123')
    assert result_status == result.ResultStatus.MODULE_FAILURE


def test_extract_and_parse_valid_input(file_path):
    """Test extract_and_parse for valid file path
    """
    module_result, result_status = common.extract_and_parse(file_path)
    assert result_status == result.ResultStatus.ALL_OKAY
    assert isinstance(module_result, dict)
    assert module_result['user_id'] == 'pewdiepie'
    assert module_result['tweet'] == 'ey send me stolen pdp wave designs'
