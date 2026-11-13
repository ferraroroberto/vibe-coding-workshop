"""The organisational hierarchy is defined once, in ``hierarchy.py``.

Run from ``metadata/``:  python -m unittest test_hierarchy
"""

import re
import unittest
from pathlib import Path

from hierarchy import HIERARCHY_LABELS, HIERARCHY_LEVELS, hierarchy_levels

HERE = Path(__file__).parent

# A hierarchy display label in any spelling: "N+3 (DT)", "N+3(dt)", "N+1 (DAN)".
LABEL_SPELLING = re.compile(r'N\+\d', re.IGNORECASE)


class HierarchyDefinitionTests(unittest.TestCase):
    def test_levels_are_unique_columns(self):
        columns = [column for column, _ in HIERARCHY_LEVELS]
        self.assertEqual(len(columns), len(set(columns)))

    def test_hierarchy_levels_keeps_the_requested_order(self):
        self.assertEqual(
            hierarchy_levels('des_dan', 'des_dt'),
            [('des_dan', HIERARCHY_LABELS['des_dan']), ('des_dt', HIERARCHY_LABELS['des_dt'])],
        )

    def test_unknown_column_is_refused(self):
        with self.assertRaises(KeyError):
            hierarchy_levels('des_nope')


class NoRespelledLabelsTests(unittest.TestCase):
    def test_only_hierarchy_module_spells_a_level_label(self):
        offenders = []
        for path in sorted(HERE.glob('*.py')):
            if path.name == 'hierarchy.py' or path.name.startswith('test_'):
                continue
            for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                if line.lstrip().startswith('#'):
                    continue
                if LABEL_SPELLING.search(line):
                    offenders.append(f'{path.name}:{number}: {line.strip()}')
        self.assertEqual(offenders, [], 'spell hierarchy labels only in hierarchy.py')


if __name__ == '__main__':
    unittest.main()
