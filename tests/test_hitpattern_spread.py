import unittest
import numpy as np

from pax import core, plugin, units
from pax.datastructure import Peak, Event
from pax.utils import empty_event


class TestComputeHitpatternSpread(unittest.TestCase):

    def setUp(self):
        self.pax = core.Processor(config_names='XENON100', just_testing=True, config_dict={'pax': {
            'plugin_group_names': ['test'],
            'test':               'ComputeHitpatternSpread.ComputeHitpatternSpread'}})
        self.plugin = self.pax.get_plugin_by_name('ComputeHitpatternSpread')

    @staticmethod
    def example_event(channels_with_something):
        bla = np.zeros(242)
        bla[np.array(channels_with_something)] = 1
        e = empty_event()
        e.peaks.append(Peak({'left':  5,
                             'right': 9,
                             'type':  'unknown',
                             'detector':  'tpc',
                             'area_per_channel': bla,
                             }))
        return e

    def test_get_plugin(self):
        self.assertIsInstance(self.plugin, plugin.TransformPlugin)
        self.assertEqual(self.plugin.__class__.__name__, 'ComputeHitpatternSpread')

    def test_compute_spread(self):
        e = self.example_event([1, 16])
        e = self.plugin.transform_event(e)
        self.assertIsInstance(e, Event)
        self.assertEqual(len(e.peaks), 1)
        p = e.peaks[0]

        # PMT 1 and 16 are aligned in y, 166.84 mm from center in x on opposite sides
        self.assertAlmostEqual(p.hitpattern_top_spread, 166.84 * units.mm / 2**0.5)

        # If no hits, hitpattern spread should be nan
        self.assertEqual(p.hitpattern_bottom_spread, 0)