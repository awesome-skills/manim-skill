"""Exercise timestamp sampling against encoded video, not a mocked decoder."""
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import subprocess
import sys

import av
from PIL import Image

from scripts.video_inspection import inspect_video, transition_times, write_review_page


class VideoInspection(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def encode(self, timestamps, size=(160, 90)):
        path = self.root / "sample.mp4"
        with av.open(str(path), "w") as container:
            stream = container.add_stream("libx264", rate=10)
            stream.width, stream.height = size
            stream.pix_fmt = "yuv420p"
            stream.options = {"bf": "0"}
            for index, timestamp in enumerate(timestamps):
                image = Image.new("RGB", size, (index * 20, 50, 100))
                frame = av.VideoFrame.from_image(image)
                frame.pts, frame.time_base = timestamp, Fraction(1, 10)
                for packet in stream.encode(frame):
                    container.mux(packet)
            for packet in stream.encode():
                container.mux(packet)
        return path

    def test_displayed_frame_boundaries_and_readable_grid(self):
        path = self.encode(range(10))
        out = self.root / "contact.png"
        report = inspect_video(path, out, [0, 0.09, 0.1, 0.25, 1.0], columns=2)
        self.assertEqual([s["frame_index"] for s in report["samples"]], [0, 0, 1, 2, 9])
        self.assertEqual(report["decoded_frames"], 10)
        self.assertEqual(report["visual_review"], "not performed")
        with Image.open(out) as image:
            self.assertEqual(image.size, (1280, 1170))

    def test_irregular_timestamps_use_presentation_time(self):
        path = self.encode([0, 2, 7, 10])
        report = inspect_video(path, self.root / "contact.png", [0.1, 0.4, 0.8])
        self.assertEqual([s["frame_index"] for s in report["samples"]], [0, 1, 2])
        for sample, expected in zip(report["samples"], [0, 0.2, 0.7]):
            self.assertAlmostEqual(sample["actual_seconds"], expected)

    def test_delivery_width_preview_preserves_portrait_and_original_frames(self):
        for size, preview_size in [((160, 90), (360, 202)), ((90, 160), (360, 640))]:
            with self.subTest(size=size):
                path = self.encode(range(10), size)
                report = inspect_video(path, self.root / "phone.png", [0.5],
                                       save_frames=True, preview_width=360)
                with Image.open(self.root / "phone.png") as sheet:
                    self.assertEqual(sheet.size, (preview_size[0], preview_size[1] + 30))
                with Image.open(report["samples"][0]["frame_path"]) as frame:
                    self.assertEqual(frame.size, size)
                self.assertEqual(report["samples"][0]["frame_index"], 5)
                self.assertEqual(report["visual_review"], "not performed")
        with self.assertRaises(ValueError):
            inspect_video(path, self.root / "invalid.png", [0.5], preview_width=0)

    def test_cli_saves_full_resolution_frames_and_report(self):
        path = self.encode(range(10))
        out = self.root / "inspection"
        script = Path(__file__).resolve().parents[1] / "scripts/video_inspection.py"
        result = subprocess.run([sys.executable, str(script), str(path), "--at", "0.25",
                                 "--output", str(out)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        import json
        report = json.loads((out / "report.json").read_text())
        self.assertEqual(report["samples"][0]["frame_index"], 2)
        with Image.open(report["samples"][0]["frame_path"]) as frame:
            self.assertEqual(frame.size, (160, 90))
        self.assertTrue(Path(report["review_player"]).is_file())

    def test_transition_neighborhood_uses_displayed_frames(self):
        path = self.encode(range(10))
        times = transition_times([0.5], radius=0.2, count=5)
        report = inspect_video(path, self.root / "contact.png", times)
        self.assertEqual([s["frame_index"] for s in report["samples"]], [3, 4, 5, 6, 7])
        with self.assertRaisesRegex(ValueError, "Sample times"):
            inspect_video(path, self.root / "contact.png", transition_times([0.05]))
        for radius, count in [(0, 5), (-1, 5), (float("nan"), 5), (0.3, 2), (0.3, 4)]:
            with self.assertRaises(ValueError):
                transition_times([0.5], radius, count)

    def test_review_player_escapes_title_and_encodes_media_path(self):
        path = self.encode(range(10))
        odd_path = self.root / 'clip <test> #1.mp4'
        path.rename(odd_path)
        report = inspect_video(odd_path, self.root / "contact.png", [0.5])
        page = self.root / "review.html"
        write_review_page(report, page)
        from html.parser import HTMLParser
        class Sources(HTMLParser):
            source = None
            def handle_starttag(self, tag, attrs):
                if tag == "video":
                    self.source = dict(attrs)["src"]
        parsed = Sources()
        parsed.feed(page.read_text())
        from urllib.parse import unquote
        self.assertEqual((page.parent / unquote(parsed.source)).resolve(), odd_path.resolve())
        self.assertIn("clip &lt;test&gt; #1.mp4", page.read_text())

    def test_unavailable_timestamp_is_reported(self):
        path = self.encode(range(10))
        with self.assertRaisesRegex(ValueError, "Sample times"):
            inspect_video(path, self.root / "contact.png", [1.1])


if __name__ == "__main__":
    unittest.main()
