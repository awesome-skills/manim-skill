#!/usr/bin/env python3
"""Decode an existing video and sample displayed frames; not visual approval."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import av
from PIL import Image, ImageDraw


def inspect_video(path, contact_path, times=None, columns=2, save_frames=False):
    """Sample the frame displayed at each time, using decoded presentation times.

    Times are seconds from the first decoded frame. The duration endpoint selects
    the last frame. Decode the whole video while retaining only requested images.
    """
    path, contact_path = Path(path), Path(contact_path)
    if columns < 1:
        raise ValueError("columns must be positive")
    samples = []
    contact_path.parent.mkdir(parents=True, exist_ok=True)
    with av.open(str(path)) as container:
        if not container.streams.video:
            raise ValueError(f"No video stream: {path}")
        stream = container.streams.video[0]
        width, height = stream.width, stream.height
        duration = float(stream.duration * stream.time_base) if stream.duration else None
        if duration is None or duration <= 0:
            raise ValueError(f"No positive video duration metadata: {path}")
        requested = [0, duration / 4, duration / 2, duration * 3 / 4, duration] if times is None else list(times)
        if not requested or any(not math.isfinite(t) or t < 0 or t > duration for t in requested):
            raise ValueError(f"Sample times must be between 0 and {duration:.6f} seconds")
        requested = sorted(set(requested))
        total, cursor = 0, 0
        first_pts = None
        previous = None

        def retain(target, frame_info):
            index, timestamp, frame = frame_info
            samples.append({"requested_seconds": target, "actual_seconds": timestamp,
                            "frame_index": index, "image": frame.to_image()})

        for index, frame in enumerate(container.decode(video=0)):
            if frame.pts is None or frame.time_base is None:
                raise ValueError("Decoded frame has no presentation timestamp")
            pts = frame.pts * frame.time_base
            if first_pts is None:
                first_pts = pts
            timestamp = float(pts - first_pts)
            # A frame stays displayed until the next presentation timestamp.
            while cursor < len(requested) and requested[cursor] < timestamp and previous is not None:
                retain(requested[cursor], previous)
                cursor += 1
            previous = (index, timestamp, frame)
            total += 1
        if previous is None or (stream.frames and total != stream.frames):
            raise ValueError(f"Incomplete video decode: {total} frames (metadata: {stream.frames})")
        while cursor < len(requested):
            retain(requested[cursor], previous)
            cursor += 1

    columns = min(columns, len(samples))
    tile_width, tile_height = 640, 390
    sheet = Image.new("RGB", (tile_width * columns, tile_height * math.ceil(len(samples) / columns)), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for slot, sample in enumerate(samples):
        image = sample.pop("image")
        if save_frames:
            frame_path = contact_path.parent / f"frame-{sample['frame_index']:06d}.png"
            image.save(frame_path)
            sample["frame_path"] = str(frame_path.resolve())
        image.thumbnail((640, 360))
        x, y = slot % columns * tile_width, slot // columns * tile_height
        sheet.paste(image, (x + (640 - image.width) // 2, y + 30 + (360 - image.height) // 2))
        draw.text((x + 8, y + 8),
                  f"want {sample['requested_seconds']:.3f}s | frame {sample['frame_index']} @ {sample['actual_seconds']:.3f}s",
                  fill="black")
    sheet.save(contact_path)
    return {"artifact": str(path.resolve()), "width": width, "height": height, "duration_seconds": duration,
            "decoded_frames": total, "bytes": path.stat().st_size,
            "video_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "contact_sheet": str(contact_path.resolve()), "samples": samples,
            "sampling": "displayed frame at requested time (presentation timestamps)",
            "visual_review": "not performed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--at", type=float, action="append", help="Seconds from first frame; repeatable")
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True, help="Directory for contact.png and report.json")
    args = parser.parse_args()
    report = inspect_video(args.video, args.output / "contact.png", args.at, args.columns, save_frames=True)
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
