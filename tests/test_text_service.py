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
    """Test get_entities for empty input
    """
    with pytest.raises(TypeError):
        data_parser.get_entities()


def test_get_entities_invalid_type_input():
    """Test get_entities for invalid type input
    """
    with pytest.raises(TypeError):
        data_parser.get_entities({1})
        data_parser.get_entities(None)
        data_parser.get_entities(['123'])


def test_get_entities_invalid_input():
    """Test get_entities for valid type invalid input
    """
    with pytest.raises(ValueError):
        data_parser.get_entities('')


def test_get_entities_valid_input():
    """Test get_entities for valid type valid extracted string
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
    module_result, module_status = data_parser.get_entities(
        test_extracted_text)
    assert module_status == result.ResultStatus.ALL_OKAY
    assert test_result_user_id == module_result['user_id']
    assert test_result_tweet in module_result['tweet']
    assert test_result_datetime == module_result['date']


def test_clean_text_empty_input():
    """Test clean_text for empty input
    """
    with pytest.raises(TypeError):
        data_parser.clean_text()


def test_clean_text_invalid_type_input():
    """Test clean_text for invalid type input
    """
    with pytest.raises(TypeError):
        data_parser.clean_text(None)
        data_parser.clean_text(123)
        data_parser.clean_text([1, '2', '3'])


def test_clean_text_invalid_input():
    """Test clean_text for valid type invalid input
    """
    with pytest.raises(ValueError):
        data_parser.clean_text('')


def test_clean_text_valid_input():
    """Test clean_text for valid input
    """
    test_str = "Ms. Tree caught the Falcon fairing!!"
    module_result, module_status = data_parser.clean_text(test_str)
    assert module_status == result.ResultStatus.ALL_OKAY
    assert module_result == "caught Falcon fairing"


def test_get_similarity_empty_input():
    """Test get_similarity for empty input
    """
    with pytest.raises(TypeError):
        text_processor.get_similarity()


def test_get_similarity_invalid_type_input():
    """Test get_similarity for invalid type input
    """
    with pytest.raises(TypeError):
        text_processor.get_similarity(123, 123)
        text_processor.get_similarity(None, None)
        text_processor.get_similarity(None, 123)
        text_processor.get_similarity([], '')


def test_get_similarity_invalid_input():
    """Test get_similarity for valid type invalid input
    """
    with pytest.raises(ValueError):
        text_processor.get_similarity('', [])


def test_get_similarity_valid_input(tweet_data):
    """Test get_similarity for valid input
    """
    from numpy import allclose, array

    test_extracted_text = "What ants must feel like pic.twitter.com/NSsBZXnEvp"
    test_result = array([[1., 0., 0., 0.09245003, 1., 0.],
                         [0., 1., 0.20412415, 0., 0., 0.],
                         [0., 0.20412415, 1., 0., 0., 0.],
                         [0.09245003, 0., 0., 1., 0.09245003, 0.],
                         [1., 0., 0., 0.09245003, 1., 0.],
                         [0., 0., 0., 0., 0., 0.]])
    module_result, module_status = text_processor.get_similarity(
        test_extracted_text, tweet_data)
    assert module_status == result.ResultStatus.ALL_OKAY
    assert allclose(module_result, test_result)
