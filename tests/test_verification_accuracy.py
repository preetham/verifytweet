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

from sklearn.metrics import accuracy_score

from verifytweet import controller
from verifytweet import result

def test_overall_accuracy(test_data):
    overall_expected_output = list()
    overall_actual_output = list()
    subset_accuracy = list()
    non_api_controller = controller.NonAPIApproach()
    for subset in test_data:
        subset_expected_output = [subset['expected_value']] * len(
            subset['files'])
        overall_expected_output.extend(subset_expected_output)
        actual_output = list()
        accuracy_dict = dict()
        for file_path in subset['files']:
            module_result, module_status = non_api_controller.exec(
                file_path)
            validity = True if module_status == result.ResultStatus.ALL_OKAY else False
            actual_output.append(validity)
            overall_actual_output.append(validity)
        accuracy_dict['type'] = subset['type']
        accuracy_dict['expected'] = subset['expected_value']
        accuracy_dict['accuracy'] = accuracy_score(subset_expected_output, actual_output)
        subset_accuracy.append(accuracy_dict)
    accuracy = accuracy_score(overall_expected_output, overall_actual_output)
    print(f'Subset Accuracy: {subset_accuracy}')
    print(f'Overall Accuracy: {accuracy}')
    assert accuracy > 0.7