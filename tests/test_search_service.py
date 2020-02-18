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

from verifytweet import search as search_service
from verifytweet import result

twitter_api_search = search_service.TwitterAPISearch()
twint_search = search_service.TwintSearch()


def test_search_empty_input():
    """Test search for empty input
    """
    with pytest.raises(TypeError):
        twint_search.search()


def test_search_invalid_type_input():
    """Test search for invalid type input
    """
    with pytest.raises(TypeError):
        twint_search.search(123)
        twint_search.search('123')
        twint_search.search(None, None, None)
        twint_search.search(['123'], [123], ['123'])
        twint_search.search('123', None, None)
        twint_search.search('123', '2019-07-06', 123)


def test_search_invalid_input():
    """Test search for valid type invalid input
    """
    with pytest.raises(ValueError):
        twint_search.search(
            '',
            '',
            datetime.datetime.now())


def test_search_valid_input():
    """Test search for valid input
    """
    test_user_id = 'elonmusk'
    test_tweet_snippet = 'Sharknado'
    test_tweet = 'Sharknado is real'
    module_result, module_status = twint_search.search(test_user_id,
                                                       test_tweet_snippet)
    assert module_status == result.ResultStatus.ALL_OKAY
    assert len(module_result) > 0
    assert isinstance(module_result[0].tweet, str)
    assert test_tweet in module_result[0].tweet
