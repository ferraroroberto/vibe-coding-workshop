"""Duplicate-name Phase 2 sync: each matched master record gets its own respondent's row.

Run from ``metadata/``:  python -m unittest test_phase_two_sync
"""

import unittest
from unittest import mock

import pandas as pd

import phase_two_sync


def _phase2_after_dedupe() -> pd.DataFrame:
    """Phase 2 frame shaped like ``_load_phase2_source`` output when names repeat.

    ``Ana`` appears twice (ids 1 and 9); sorting by name then id descending and
    keeping the first row leaves labels [2, 3, 1] that no longer equal positions.
    """
    raw = pd.DataFrame({
        '0': [1, 5, 7, 9],
        '1': ['Ana Lopez', 'Zoe Martin', 'Bruno Diaz', 'Ana Lopez'],
        '2': ['old answer', 'zoe answer', 'bruno answer', 'new answer'],
    })
    return raw.sort_values(by=['1', '0'], ascending=[True, False]).drop_duplicates(
        subset=['1'], keep='first')


class DuplicateNameSyncTest(unittest.TestCase):
    def test_each_match_reads_its_own_phase2_row(self):
        df_phase2 = _phase2_after_dedupe()
        self.assertEqual(list(df_phase2.index), [3, 2, 1])

        df_master = pd.DataFrame({
            'id': [10, 20, 30],
            'name': ['Ana Lopez', 'Bruno Diaz', 'Zoe Martin'],
        })
        matched, unmatched = phase_two_sync.match_phase2_to_phase1(df_master, df_phase2, '1')
        self.assertTrue(unmatched.empty)

        full_df = pd.DataFrame({'id': [10, 20, 30], 'answer': [None, None, None]})
        seen = {}

        def fake_replicate(rules, get_source, set_excel, **kwargs):
            seen[get_source('1')] = get_source('2')

        config = {'phase_two_spec': {}}
        with mock.patch.object(phase_two_sync, 'load_full_sheet', return_value=full_df), \
                mock.patch.object(phase_two_sync, 'find_id_column_name', return_value='id'), \
                mock.patch.object(phase_two_sync, 'atomic_write_sheet'), \
                mock.patch.object(phase_two_sync, 'apply_replicate_rules', side_effect=fake_replicate), \
                mock.patch.object(phase_two_sync, 'apply_binary_checks'), \
                mock.patch.object(phase_two_sync, 'st'):
            result = phase_two_sync.sync_phase2_data(df_master, matched, df_phase2, config)

        self.assertIsNotNone(result)
        self.assertEqual(seen, {
            'Ana Lopez': 'new answer',
            'Bruno Diaz': 'bruno answer',
            'Zoe Martin': 'zoe answer',
        })


if __name__ == '__main__':
    unittest.main()
