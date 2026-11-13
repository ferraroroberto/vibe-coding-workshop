"""Candidate selection status: one row per flag combination, and the refused illegal states.

Run from ``metadata/``:  python -m unittest test_selection_status
"""

import unittest

import pandas as pd
from selection_status import (
    CandidateStatus,
    candidate_status,
    exclusive_flags,
    status_column,
    status_counts,
    status_table,
)

BLANK = float('nan')

# (ind_session, ind_waitlist, expected status): every combination of 0, 1 and blank.
STATUS_TABLE = [
    (0, 0, 'Pending'),
    (1, 0, 'Selected'),
    (0, 1, 'Waitlist'),
    (1, 1, 'Conflict'),
    (BLANK, 0, 'Unknown'),
    (0, BLANK, 'Unknown'),
    (BLANK, 1, 'Unknown'),
    (1, BLANK, 'Unknown'),
    (BLANK, BLANK, 'Unknown'),
    (None, 0, 'Unknown'),
    (2, 0, 'Unknown'),
    (0, -1, 'Unknown'),
    ('1', '0', 'Selected'),
    ('x', '0', 'Unknown'),
    (1.0, 0.0, 'Selected'),
    (True, False, 'Selected'),
]


def _frame(pairs):
    return pd.DataFrame({
        'id': range(len(pairs)),
        'ind_session': [p[0] for p in pairs],
        'ind_waitlist': [p[1] for p in pairs],
    })


class CandidateStatusTest(unittest.TestCase):
    def test_every_flag_combination(self):
        for session, waitlist, expected in STATUS_TABLE:
            with self.subTest(session=session, waitlist=waitlist):
                row = {'ind_session': session, 'ind_waitlist': waitlist}
                self.assertEqual(candidate_status(row), expected)
                self.assertIsInstance(candidate_status(row), CandidateStatus)

    def test_missing_columns_read_as_unset(self):
        self.assertIs(candidate_status({}), CandidateStatus.PENDING)
        self.assertIs(candidate_status({'ind_session': 1}), CandidateStatus.SELECTED)

    def test_counts_keep_the_old_numbers_when_at_most_one_flag_is_set(self):
        pairs = [(0, 0), (1, 0), (1, 0), (0, 1), (0, 0), (0, 0), (0, 1)]
        df = _frame(pairs)
        old_selected = int((df['ind_session'] == 1).sum())
        old_waitlist = int(((df['ind_waitlist'] == 1) & (df['ind_session'] != 1)).sum())
        counts = status_counts(df)
        self.assertEqual(counts['total'], len(df))
        self.assertEqual(counts['selected'], old_selected)
        self.assertEqual(counts['waitlist'], old_waitlist)
        self.assertEqual(counts['pending'], len(df) - old_selected - old_waitlist)
        self.assertEqual((counts['conflict'], counts['unknown']), (0, 0))

    def test_a_conflict_row_is_counted_once_and_in_no_other_state(self):
        df = _frame([(1, 1), (1, 0), (0, 0)])
        counts = status_counts(df)
        self.assertEqual(
            (counts['selected'], counts['waitlist'], counts['pending'], counts['conflict']),
            (1, 0, 1, 1))
        parts = sum(counts[key] for key in ('selected', 'waitlist', 'pending', 'conflict', 'unknown'))
        self.assertEqual(parts, counts['total'])

    def test_empty_frame_counts_zero(self):
        counts = status_counts(_frame([]))
        self.assertEqual(set(counts.values()), {0})
        self.assertTrue(status_column(_frame([])).empty)

    def test_every_reader_gets_the_same_numbers_for_the_same_rows(self):
        df = _frame([(1, 1), (1, 0), (0, 1), (0, 0), (0, 0)])
        df['team'] = ['a', 'a', 'a', 'b', 'b']
        table = status_table(df, 'team').set_index('team')
        for key in ('selected', 'waitlist', 'pending', 'conflict', 'unknown'):
            self.assertEqual(int(table[key].sum()), status_counts(df)[key])

    def test_status_table_skips_blank_groups_and_keeps_columns_when_empty(self):
        df = _frame([(0, 0), (1, 0)])
        df['team'] = ['a', None]
        self.assertEqual(list(status_table(df, 'team')['team']), ['a'])
        empty = status_table(df.iloc[0:0], 'team')
        self.assertEqual(list(empty.columns[:2]), ['team', 'total'])
        self.assertTrue(empty.empty)


class IllegalTransitionTest(unittest.TestCase):
    def test_both_flags_are_never_saved_as_set(self):
        """state-machine-proof: candidate_status"""
        for session in (0, 1):
            for waitlist in (0, 1):
                for was_session in (0, 1):
                    for was_waitlist in (0, 1):
                        with self.subTest(new=(session, waitlist), was=(was_session, was_waitlist)):
                            saved = exclusive_flags(session, waitlist, was_session, was_waitlist)
                            self.assertNotEqual(saved, (1, 1))
                            row = {'ind_session': saved[0], 'ind_waitlist': saved[1]}
                            self.assertIsNot(candidate_status(row), CandidateStatus.CONFLICT)

    def test_the_flag_ticked_last_wins(self):
        self.assertEqual(exclusive_flags(1, 1, 1, 0), (0, 1))  # waitlist ticked on a Selected row
        self.assertEqual(exclusive_flags(1, 1, 0, 1), (1, 0))  # selected ticked on a Waitlist row
        self.assertEqual(exclusive_flags(1, 1, 0, 0), (1, 0))  # both ticked at once: Selected wins
        self.assertEqual(exclusive_flags(1, 1, 1, 1), (1, 0))  # an old conflict saved untouched
        self.assertEqual(exclusive_flags(0, 1, 0, 0), (0, 1))
        self.assertEqual(exclusive_flags(0, 0, 1, 0), (0, 0))

    def test_a_conflict_row_cannot_be_read_as_selected_or_waitlist(self):
        """state-machine-proof: candidate_status"""
        status = candidate_status({'ind_session': 1, 'ind_waitlist': 1})
        self.assertIs(status, CandidateStatus.CONFLICT)
        self.assertNotIn(status, (CandidateStatus.SELECTED, CandidateStatus.WAITLIST))


if __name__ == '__main__':
    unittest.main()
