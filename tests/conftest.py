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


@pytest.fixture
def test_data():
    import subprocess
    from verifytweet import util

    local_dir_path = os.path.abspath('./tests/static/test-dataset')
    cmd_process = subprocess.run([
        'aws', 's3', 'sync', 's3://verifytweet-dataset',
        os.path.abspath(local_dir_path)
    ])
    cmd_process.check_returncode()
    dataset = list()
    for (dirpath, dirnames, filenames) in os.walk(local_dir_path):
        if filenames:
            subset = dict()
            subset_type = dirpath.split('/')[-1]
            subset_truth = True if dirpath.split('/')[-2] == "real" else False
            file_paths = list()
            for filename in filenames:
                if util.uploader.allowed_file(filename):
                    file_paths.append(os.path.join(os.path.abspath(dirpath), filename))
            subset['expected_value'] = subset_truth
            subset['type'] = subset_type
            subset['files'] = file_paths
            dataset.append(subset)
    return dataset
