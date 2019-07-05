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
import datetime

from verifytweet import date_checker


def test_valid_date_empty_input():
    """Test for empty input in valid_date
    """
    with pytest.raises(TypeError):
        date_checker.valid_date()


def test_valid_date_invalid_type_input():
    """Test for invalid type input in valid_date
    """
    assert date_checker.valid_date(None) == False
    assert date_checker.valid_date('2018/02/23') == False
    assert date_checker.valid_date(2018) == False


def test_valid_date_invalid_input():
    """Test for invalid input in valid_date
    """
    test_date_str = 'Jan 01 1970 7:40AM'
    test_date_obj = datetime.datetime.strptime(
        test_date_str,
        '%b %d %Y %I:%M%p').replace(tzinfo=datetime.timezone.utc)
    assert date_checker.valid_date(test_date_obj) == False


def test_valid_date_valid_input():
    """Test for valid date in valid_date
    """
    test_date_obj = datetime.datetime.now(datetime.timezone.utc)
    assert date_checker.valid_date(test_date_obj) == True


def test_format_for_date_empty_input():
    """Test for empty input in format_for_date
    """
    with pytest.raises(TypeError):
        date_checker.format_for_date()


def test_format_for_date_invalid_type_input():
    """Test for invalid type input in format_for_date
    """
    with pytest.raises(TypeError):
        date_checker.format_for_date(None)
        date_checker.format_for_date('2018/02/23')
        date_checker.format_for_date(2018)


def test_format_for_date_valid_input():
    """Test for valid input in format_for_date
    """
    test_date_obj = datetime.datetime.now(datetime.timezone.utc)
    test_date_str = date_checker.format_for_date(test_date_obj)
    formatted_date_obj = datetime.datetime.strptime(
        test_date_str, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
    assert test_date_obj.year == formatted_date_obj.year
    assert test_date_obj.month == formatted_date_obj.month
    assert test_date_obj.day == formatted_date_obj.day
