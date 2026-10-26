"""Semantic checks that rendering alone cannot establish."""
import unittest
from manim import Sector, tempconfig
from examples.quicksort import QuickSortBars


class ExampleSemantics(unittest.TestCase):
    def test_quicksort_events_preserve_values_and_finish_sorted(self):
        with tempconfig({"format": "none"}):
            scene = QuickSortBars()
        for data in [[], [1], [3, 1, 2], [2, 2, 1], [4, 3, 2, 1], [-2, 0, -1]]:
            with self.subTest(data=data):
                events = scene.build_events(data)
                self.assertEqual(events[-1].array, sorted(data))
                self.assertEqual(events[-1].sorted_indices, tuple(range(len(data))))
                for event in events:
                    self.assertEqual(sorted(event.array), sorted(data))
                    for index in event.sorted_indices:
                        self.assertEqual(event.array[index], sorted(data)[index])
                self.assertEqual(data, events[0].array)

    def test_sector_radius_example(self):
        sector = Sector(radius=1)
        self.assertGreater(sector.width, 0)


if __name__ == "__main__":
    unittest.main()
