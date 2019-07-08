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

from twint.tweet import tweet

from verifytweet import object_mapper

def test_map_keys_empty_input():
    """Test for empty input in map_keys
    """
    with pytest.raises(TypeError):
        object_mapper.map_keys()

def test_map_keys_invalid_type_input():
    """Test for invalid type input in map_keys
    """
    with pytest.raises(TypeError):
        object_mapper.map_keys(None)
        object_mapper.map_keys(dict({
            "id": "dummy",
            "tweet": "dummy"
        }))
        object_mapper.map_keys(["id", "dummy"])

def test_map_keys_invalid_input():
    """Test for valid type, invalid input in map_keys
    """
    test_tweet_obj = tweet()
    with pytest.raises(ValueError):
        object_mapper.map_keys(test_tweet_obj)

def test_map_keys_valid_input():
    """Test for valid type, valid input in map_keys
    """
    test_tweet_obj = tweet()
    test_id = "1234"
    test_username = "twitter"
    test_tweet = "Hello World!"
    test_result = dict({
        "id": test_id,
        "username": test_username,
        "tweet": test_tweet
    })
    test_tweet_obj.id = test_id
    test_tweet_obj.conversation_id = str()
    test_tweet_obj.username = test_username
    test_tweet_obj.datetime = datetime.datetime.now()
    test_tweet_obj.datestamp = str()
    test_tweet_obj.timestamp = str()
    test_tweet_obj.user_id = str()
    test_tweet_obj.name = str()
    test_tweet_obj.place = None
    test_tweet_obj.timezone = str()
    test_tweet_obj.mentions = list()
    test_tweet_obj.urls = list()
    test_tweet_obj.photos = list()
    test_tweet_obj.video = list()
    test_tweet_obj.tweet = test_tweet
    test_tweet_obj.hashtags = list()
    test_tweet_obj.replies_count = str()
    test_tweet_obj.retweets_count = str()
    test_tweet_obj.likes_count = str()
    test_tweet_obj.link = str()
    test_tweet_obj.retweet = str()
    result, module_status = object_mapper.map_keys(test_tweet_obj)
    assert result["id"] == test_result["id"]
    assert result["username"] == test_result["username"]
    assert result["tweet"] == test_result["tweet"]
