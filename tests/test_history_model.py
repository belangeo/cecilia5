"""Property patches must preserve unrelated edits without GUI dependencies."""
import copy
import unittest
from Resources.SessionHistory import differences, merge_changes


class PropertyHistoryTests(unittest.TestCase):
    def test_nested_fields_preserve_later_runtime_updates(self):
        before = {'slider': [.5, 0, None, 1], 'other': 1}
        after = {'slider': [.8, 0, None, 1], 'other': 1}
        changes = differences(before, after)
        current = {'slider': [.9, 0, 12, 1], 'other': 7}
        result = merge_changes(current, changes, False)
        self.assertEqual(result, {'slider': [.5, 0, 12, 1], 'other': 7})
        self.assertEqual(current['slider'][0], .9)
        self.assertEqual(merge_changes(result, changes, True)['slider'][0], .8)

    def test_dictionary_insert_remove_and_curve_snapshot_are_immutable(self):
        before = {'a': 1, 'userGraph': {'env': {'data': [[0, 0], [1, 1]]}}}
        after = {'b': 2, 'userGraph': {'env': {'data': [[0, .5], [1, 1]]}}}
        expected = copy.deepcopy(after)
        changes = differences(before, after)
        after['userGraph']['env']['data'][0][1] = .9
        self.assertEqual(merge_changes(before, changes, True), expected)
        self.assertEqual(merge_changes(expected, changes, False), before)
