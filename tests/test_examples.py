"""Semantic checks that rendering alone cannot establish."""
import unittest
from manim import Sector, tempconfig
from examples.quicksort import QuickSortBars
from examples.merge_step import merge_trace
from examples.wave_superposition import wave_values
from examples.local_linearity import curve_y, tangent_y
from examples.damping_story import spring_state
from examples.bezier_construction import quadratic_construction
from examples.packet_journey import PacketJourney
from examples.motion_timing import MotionTiming
from manim import config
import numpy as np


class ExampleSemantics(unittest.TestCase):
    def test_quadratic_construction_matches_bernstein_and_endpoints(self):
        points = np.array([[-2., 0, 0], [1., 4, 0], [5., -1, 0]])
        for t in np.linspace(0, 1, 21):
            _, result = quadratic_construction(points, t)
            expected = (1-t)**2*points[0] + 2*t*(1-t)*points[1] + t*t*points[2]
            np.testing.assert_allclose(result, expected, atol=1e-12)
        np.testing.assert_allclose(quadratic_construction(points, 0)[1], points[0])
        np.testing.assert_allclose(quadratic_construction(points, 1)[1], points[2])

    def test_spring_release_obeys_motion_and_energy_balance(self):
        times = np.linspace(0, 10, 1001)
        omega, amplitude = 2.4, 1.35
        for damping in [0, .32, .8]:
            x, velocity, energy = spring_state(times, damping)
            self.assertAlmostEqual(float(x[0]), amplitude)
            self.assertAlmostEqual(float(velocity[0]), 0)
            self.assertAlmostEqual(float(energy[0]), 1)
            dt = 1e-5
            after = spring_state(times + dt, damping)
            back = spring_state(times - dt, damping)
            np.testing.assert_allclose((after[0]-back[0])/(2*dt), velocity, atol=1e-8)
            acceleration = (after[1]-back[1])/(2*dt)
            np.testing.assert_allclose(acceleration + 2*damping*omega*velocity + omega**2*x, 0, atol=1e-8)
            expected_loss = -4*damping*velocity**2/(omega*amplitude**2)
            np.testing.assert_allclose((after[2]-back[2])/(2*dt), expected_loss, atol=1e-8)
            if damping == 0:
                np.testing.assert_allclose(energy, 1, atol=1e-12)
            else:
                self.assertTrue(np.all(np.diff(energy) <= 1e-12))

    def test_local_tangent_matches_point_and_error_shrinks_quadratically(self):
        for anchor in [-2.0, 0.0, 1.0, 3.0]:
            self.assertAlmostEqual(float(tangent_y(anchor, anchor)), float(curve_y(anchor)))
            epsilon = 1e-4
            numerical_slope = (curve_y(anchor + epsilon) - curve_y(anchor - epsilon)) / (2 * epsilon)
            self.assertAlmostEqual(float(tangent_y(anchor + 1, anchor) - tangent_y(anchor, anchor)),
                                   float(numerical_slope), places=8)
            for distance in [-1.0, -0.5, 0.5, 1.0]:
                error = curve_y(anchor + distance) - tangent_y(anchor + distance, anchor)
                near_error = curve_y(anchor + distance / 2) - tangent_y(anchor + distance / 2, anchor)
                self.assertGreater(float(error), 0)
                self.assertAlmostEqual(float(error), 4 * float(near_error))

    def test_portrait_camera_uses_requested_aspect_without_global_leak(self):
        for scene_type in [PacketJourney, MotionTiming]:
            with self.subTest(scene=scene_type.__name__):
                with tempconfig({"format": "none", "pixel_width": 720, "pixel_height": 1280}):
                    original_width = config.frame_width
                    scene = scene_type()
                    self.assertAlmostEqual(scene.camera.frame_width / scene.camera.frame_height, 9 / 16)
                    self.assertAlmostEqual(scene.camera.frame_height, config.frame_height)
                    self.assertEqual(config.frame_width, original_width)

    def test_merge_preserves_source_identity_and_stable_ties(self):
        for left, right in [([], []), ([], [1]), ([2, 5, 8], [3, 6, 9]),
                            ([-2, 2, 2], [-1, 2])]:
            with self.subTest(left=left, right=right):
                events = merge_trace(left, right)
                self.assertEqual([e[2] for e in events], sorted(left + right))
                self.assertEqual(len(set((s, i) for s, i, _ in events)), len(left + right))
                for side, index, value in events:
                    self.assertEqual(value, (left if side == "left" else right)[index])
        self.assertEqual(merge_trace([2, 2], [2]),
                         [("left", 0, 2), ("left", 1, 2), ("right", 0, 2)])

    def test_superposition_alignment_and_cancellation(self):
        xs = np.linspace(-5, 5, 101)
        for phase in [0, 0.7, np.pi, 2 * np.pi]:
            a, b, total = wave_values(xs, phase)
            np.testing.assert_allclose(total, a + b)
        np.testing.assert_allclose(wave_values(xs, 0)[2], 1.75 * np.sin(xs), atol=1e-12)
        np.testing.assert_allclose(wave_values(xs, np.pi)[2], 0.25 * np.sin(xs), atol=1e-12)

    def test_quicksort_swap_moves_existing_values_without_resizing(self):
        from unittest.mock import patch
        with tempconfig({"format": "none"}):
            scene = QuickSortBars()
        bars, labels, _ = scene.build_bars(scene.build_events([1, 4, 2])[0], 3, 4)
        original_bars, original_labels = list(bars), list(labels)
        heights = [bar.height for bar in bars]
        initial_x = [bar.get_x() for bar in bars]

        def sample_motion(*animations, **kwargs):
            for animation in animations:
                animation.begin()
            for alpha in [0, .25, .5, .75, 1]:
                for animation in animations:
                    animation.interpolate(alpha)
                np.testing.assert_allclose([bar.height for bar in bars], heights)
                self.assertEqual([label.text for label in labels], ["1", "4", "2"])
            for animation in animations:
                animation.finish()

        with patch.object(scene, "play", side_effect=sample_motion):
            scene.move_swap(bars, labels, 0, 1)
        self.assertIs(bars[1], original_bars[0])
        self.assertIs(labels[1], original_labels[0])
        self.assertIs(bars[0], original_bars[1])
        np.testing.assert_allclose([bar.get_x() for bar in bars], initial_x)
        self.assertEqual([label.text for label in labels], ["4", "1", "2"])

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
