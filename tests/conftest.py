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
import os


@pytest.fixture
def file_path():
    return os.path.abspath('./tests/static/real-tweet.png')


@pytest.fixture
def tweet_data():
    import csv

    tweet_list = list()
    with open(os.path.abspath('./tests/static/tweets.csv'),
              newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            tweet_list.append(row[10])
    return tweet_list[1:]
