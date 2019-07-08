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

from werkzeug.datastructures import FileStorage

from verifytweet import uploader
from verifytweet import settings


def test_save_to_disk_empty_input():
    """Test save to disk for empty input
    """
    with pytest.raises(TypeError):
        uploader.save_to_disk()


def test_save_to_disk_invalid_type_input():
    """Test save to disk for invalid input type
    """
    with pytest.raises(TypeError):
        uploader.save_to_disk('')
        uploader.save_to_disk('123')
        uploader.save_to_disk(None)
        uploader.save_to_disk(123)


def test_save_to_disk_invalid_input():
    """Test save to disk for invalid input of valid type
    """
    test_file_obj = FileStorage('123')
    with pytest.raises(ValueError):
        uploader.save_to_disk(test_file_obj)


def test_save_to_disk_valid_input(file_path):
    """Test save to disk for valid file object
    """
    app_config = settings.app_config
    app_config.ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

    with open(file_path, 'rb') as f:
        test_file_obj = FileStorage(f)
        test_file_name = uploader.save_to_disk(test_file_obj)
    assert isinstance(test_file_name, str)
