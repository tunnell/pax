import unittest

import numpy as np

from pax import utils


class TestDSPUtils(unittest.TestCase):
    def test_where_changes_without_report_first_index(self):
        for example, result in (
                # example                           #b_f           #b_t
                ([0, 1, 2, 0, 4, -1, 60, 700, -4], ([3, 5, 8], [1, 4, 6])),
                ([1, 1, 2, 0, 4, -1, 60, 700, -4], ([3, 5, 8], [4, 6])),
                ([1, 0, 2, 3, 4, -1, 60, 700, -4], ([1, 5, 8], [2, 6])),
                ([1, 0, 2, 3, 4, -1, 60, 700, 800], ([1, 5], [2, 6])),
                ([0, 0, 2, 3, 4, -1, 60, 700, 800], ([5], [2, 6])),
                ([1], ([], [])),
                ([0], ([], [])),
                ([0, 0], ([], [])),
                ([1, 1], ([], [])),
                ([0, 1, 1], ([], [1])),
        ):
            # Separate results
            b_t, b_f = utils.where_changes(np.array(example) > 0)
            self.assertEqual(list(b_f), result[0])
            self.assertEqual(list(b_t), result[1])

            # Not separate results
            it_was = list(utils.where_changes(np.array(example) > 0,
                                              separate_results=False))
            it_should_be = sorted(result[0] + result[1])
            self.assertEqual(it_was, it_should_be)

    def test_where_changes_with_report_first_index_false(self):
        for example, result in (
                # example                           #b_f           #b_t
                ([0, 1, 2, 0, 4, -1, 60, 700, -4], ([0, 3, 5, 8], [1, 4, 6])),
                ([1, 1, 2, 0, 4, -1, 60, 700, -4], ([3, 5, 8], [4, 6])),
                ([1, 0, 2, 3, 4, -1, 60, 700, -4], ([1, 5, 8], [2, 6])),
                ([1, 0, 2, 3, 4, -1, 60, 700, 800], ([1, 5], [2, 6])),
                ([0, 0, 2, 3, 4, -1, 60, 700, 800], ([0, 5], [2, 6])),
                ([1], ([], [])),
                ([0], ([0], [])),
                ([0, 0], ([0], [])),
                ([1, 1], ([], [])),
                ([0, 1, 1], ([0], [1])),
        ):
            b_t, b_f = utils.where_changes(np.array(example) > 0,
                                           report_first_index_if=False)
            self.assertEqual(list(b_f), result[0])
            self.assertEqual(list(b_t), result[1])

            it_was = list(utils.where_changes(np.array(example) > 0,
                                              report_first_index_if=False,
                                              separate_results=False))
            it_should_be = sorted(result[0] + result[1])
            self.assertEqual(it_was, it_should_be)

    def test_where_changes_with_report_first_index_true(self):
        for example, result in (
                # example                          #b_f        #b_t
                ([0, 1, 2, 0, 4, -1, 60, 700, -4], ([3, 5, 8], [1, 4, 6])),
                ([1, 1, 2, 0, 4, -1, 60, 700, -4], ([3, 5, 8], [0, 4, 6])),
                ([1, 0, 2, 3, 4, -1, 60, 700, -4], ([1, 5, 8], [0, 2, 6])),
                ([1, 0, 2, 3, 4, -1, 60, 700, 800], ([1, 5], [0, 2, 6])),
                ([0, 0, 2, 3, 4, -1, 60, 700, 800], ([5], [2, 6])),
                ([1], ([], [0])),
                ([0], ([], [])),
                ([0, 0], ([], [])),
                ([1, 1], ([], [0])),
                ([0, 1, 1], ([], [1])),
        ):
            b_t, b_f = utils.where_changes(np.array(example) > 0,
                                           report_first_index_if=True)
            self.assertEqual(list(b_f), result[0])
            self.assertEqual(list(b_t), result[1])

            it_was = list(utils.where_changes(np.array(example) > 0,
                                              report_first_index_if=True,
                                              separate_results=False))
            it_should_be = sorted(result[0] + result[1])
            self.assertEqual(it_was, it_should_be)

    def test_intervals_where(self):
        self.assertEqual(utils.intervals_where([True]), [(0, 0)])
        self.assertEqual(utils.intervals_where([False]), [])
        self.assertEqual(utils.intervals_where([False, False]), [])
        self.assertEqual(utils.intervals_where([True, True]), [(0, 1)])
        self.assertEqual(utils.intervals_where([False, True, True]), [(1, 2)])
        self.assertEqual(utils.intervals_where([False, False, True]), [(2, 2)])

        example = np.array([0, 1, 2, 0, 4, -1, 60, 700, -4])
        self.assertEqual(utils.intervals_where(example > 0),
                         [(1, 2), (4, 4), (6, 7)])

        example = np.array([1, 1, 2, 0, 4, -1, 60, 700, -4])
        self.assertEqual(utils.intervals_where(example > 0),
                         [(0, 2), (4, 4), (6, 7)])

        example = np.array([1, 0, 2, 3, 4, -1, 60, 700, -4])
        self.assertEqual(utils.intervals_where(example > 0),
                         [(0, 0), (2, 4), (6, 7)])

        example = np.array([1, 0, 2, 3, 4, -1, 60, 700, 800])
        self.assertEqual(utils.intervals_where(example > 0),
                         [(0, 0), (2, 4), (6, 8)])

        example = np.array([0, 0, 2, 3, 4, -1, 60, 700, 800])
        self.assertEqual(utils.intervals_where(example > 0), [(2, 4), (6, 8)])

    def test_chunk_in_ntuples(self):

        # Perfect fits
        self.assertEqual(utils.chunk_in_ntuples('abcd', 2, 'x'), [('a', 'b'),
                                                                  ('c', 'd'), ])
        self.assertEqual(utils.chunk_in_ntuples('abcdefg', 1, 'x'),
                         [('a',), ('b',), ('c',), ('d',), ('e',), ('f',),
                          ('g',)])
        self.assertEqual(utils.chunk_in_ntuples('abcdefg', 7, 'x'),
                         [('a', 'b', 'c', 'd', 'e', 'f', 'g')])

        # Imperfect fits
        self.assertEqual(utils.chunk_in_ntuples('abcdefg', 3, 'x'),
                         [('a', 'b', 'c'), ('d', 'e', 'f'), ('g', 'x', 'x')])
        self.assertEqual(utils.chunk_in_ntuples('abcdefg', 2, 'x'),
                         [('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'x')])
        self.assertEqual(utils.chunk_in_ntuples('abcdefg', 8, 'x'),
                         [('a', 'b', 'c', 'd', 'e', 'f', 'g', 'x')])

        # Insane input values
        self.assertRaises(ValueError, utils.chunk_in_ntuples, 'abcdefg', 0, 'x')

        # Numpy
        self.assertEqual(utils.chunk_in_ntuples(np.array(list('abc')), 2, 'x'),
                         [('a', 'b'), ('c', 'x'), ])

    def test_cluster_by_diff(self):

        example = [-100, 2, 3, 40, 40.5, 41, 100, 101]
        self.assertEqual(
            list(map(list, utils.cluster_by_diff(example, 10))),
            [[-100, ], [2, 3], [40, 40.5, 41, ], [100, 101, ]]
        )

        # return indices
        self.assertEqual(
            list(map(list,
                     utils.cluster_by_diff(example, 10, return_indices=True))),
            [[0, ], [1, 2], [3, 4, 5, ], [6, 7, ]]
        )

        # numpy input
        example = np.array(example)
        self.assertEqual(
            list(map(list, utils.cluster_by_diff(example, 10))),
            [[-100, ], [2, 3], [40, 40.5, 41, ], [100, 101, ]]
        )

        # unsorted input
        # Don't do shuffling here, don't want a nondeterministic test!
        example = [2.0, -100.0, 40.5, 40.0, 3.0, 101.0, 41.0, 100.0]
        self.assertEqual(
            list(map(list, utils.cluster_by_diff(example, 10))),
            [[-100, ], [2, 3], [40, 40.5, 41, ], [100, 101, ]]
        )