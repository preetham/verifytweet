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

from verifytweet import text as text_service
from verifytweet import result

data_parser = text_service.DataParser()
text_processor = text_service.TextProcessor()

def test_get_entities_empty_input():
    """Test get entities for empty input
    """
    with pytest.raises(TypeError):
        data_parser.get_entities()


def test_get_entities_invalid_type_input():
    """Test get entities for invalid type input
    """
    with pytest.raises(TypeError):
        data_parser.get_entities({1})
        data_parser.get_entities(None)
        data_parser.get_entities(['123'])


def test_get_entities_invalid_input():
    """Test get entities for valid type invalid input
    """
    with pytest.raises(ValueError):
        data_parser.get_entities('')


def test_get_entities_valid_input():
    """Test get entities for valid type valid extracted string
    """
    test_extracted_text = """ 

        Elon Musk @
        © @elonmusk CC ¥
        Ms. Tree caught the Falcon fairing!!

        1:21 AM - 25 Jun 2019

        

        2,174 Retweets 42,613 Likes oO ome C wo

        © 10K fT) 22K © 48K M4

    """
    test_result_user_id = 'elonmusk'
    test_result_tweet = 'Ms. Tree caught the Falcon fairing!!'
    test_result_datetime = datetime.datetime(2019,
                                      6,
                                      25,
                                      1,
                                      21,
                                      tzinfo=datetime.timezone.utc)
    module_result, module_status = data_parser.get_entities(test_extracted_text)
    assert module_status == result.ResultStatus.ALL_OKAY
    assert test_result_user_id == module_result['user_id']
    assert test_result_tweet in module_result['tweet']
    assert test_result_datetime == module_result['date']
