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

from verifytweet import image as image_service
from verifytweet import result

extractor = image_service.Extractor()

def test_get_text_empty_input():
    """Test get_text for empty input
    """
    with pytest.raises(TypeError):
        extractor.get_text()


def test_get_text_invalid_type_input():
    """Test get_text for invalid type input
    """
    with pytest.raises(TypeError):
        extractor.get_text(None)
        extractor.get_text(123)
        extractor.get_text(['123'])


def test_get_text_invalid_input():
    """Test get_text for valid type invalid input
    """
    with pytest.raises(ValueError):
        extractor.get_text('')
    assert extractor.get_text('123')[1] == result.ResultStatus.MODULE_FAILURE
    assert extractor.get_text('/home')[1] == result.ResultStatus.MODULE_FAILURE
    assert extractor.get_text('tmp.')[1] == result.ResultStatus.MODULE_FAILURE


def test_get_text_valid_input(file_path):
    """Test get_text for valid input
    """
    test_result = "ey send me stolen pdp wave designs"
    module_result, module_status = extractor.get_text(file_path)
    assert module_status == result.ResultStatus.ALL_OKAY
    assert test_result in module_result
