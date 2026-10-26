"""Exercise timestamp sampling against encoded video, not a mocked decoder."""
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import subprocess
import sys

import av
from PIL import Image

from scripts.video_inspection import inspect_video


class VideoInspection(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def encode(self, timestamps):
        path = self.root / "sample.mp4"
        with av.open(str(path), "w") as container:
            stream = container.add_stream("libx264", rate=10)
            stream.width, stream.height = 160, 90
            stream.pix_fmt = "yuv420p"
            stream.options = {"bf": "0"}
            for index, timestamp in enumerate(timestamps):
                image = Image.new("RGB", (160, 90), (index * 20, 50, 100))
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

    def test_unavailable_timestamp_is_reported(self):
        path = self.encode(range(10))
        with self.assertRaisesRegex(ValueError, "Sample times"):
            inspect_video(path, self.root / "contact.png", [1.1])


if __name__ == "__main__":
    unittest.main()
