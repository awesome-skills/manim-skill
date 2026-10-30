#!/usr/bin/env python3
"""Decode an existing video and sample displayed frames; not visual approval."""
import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
from urllib.parse import quote

import av
from PIL import Image, ImageDraw


def transition_times(centers, radius=0.3, count=5):
    """Include both sides of a transition; invalid video bounds fail at inspection."""
    if not math.isfinite(radius) or radius <= 0 or count < 3 or count % 2 == 0:
        raise ValueError("Transition radius must be positive; count must be odd and at least 3")
    return [center - radius + 2 * radius * i / (count - 1)
            for center in centers for i in range(count)]


def write_review_page(report, output):
    """A local native-video player for the exact inspected artifact, with bookmarks."""
    output = Path(output).resolve()
    video = Path(report["artifact"]).resolve()
    # URL-encode paths and HTML-escape all interpolated text; no CDN or upload.
    relative = os.path.relpath(video, output.parent)
    src = html.escape(quote(Path(relative).as_posix()), quote=True)
    title = html.escape(video.name)
    buttons = "\n".join(
        f'<button data-time="{s["requested_seconds"]:.9f}">'
        f'{s["requested_seconds"]:.3f}s</button>' for s in report["samples"]
    )
    output.write_text(f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Review · {title}</title>
<style>
body{{margin:0;background:#101923;color:#eaf1f4;font:16px system-ui,sans-serif}}
main{{max-width:1120px;margin:auto;padding:24px}}h1{{font-size:24px}}
video{{display:block;width:100%;max-height:72vh;background:#000}}
nav{{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}}
button,select{{background:#253a49;color:#fff;border:1px solid #638399;border-radius:6px;padding:8px}}
p{{color:#b4c7d2;line-height:1.5}}code{{overflow-wrap:anywhere}}button:focus-visible{{outline:3px solid #e9b775}}
</style><main><h1>{title}</h1>
<video controls preload="metadata" src="{src}"></video>
<nav aria-label="Requested inspection times">{buttons}</nav>
<label>Playback speed <select><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="1.5">1.5×</option></select></label>
<p>{report["width"]} × {report["height"]} · {report["duration_seconds"]:.3f}s · {report["decoded_frames"]} decoded frames</p>
<p>Review at 1× for pacing; use bookmarks for transitions. Opening this page does not record visual acceptance.
The PNG samples and report.json contain the decoded frame timestamps; browser seeking is a playback aid.</p>
<p>Inspected SHA-256: <code>{report["video_sha256"]}</code></p>
<p>Keep this page with its original video path. Re-inspect after replacing the video.</p></main>
<script>
const video=document.querySelector('video');
for(const button of document.querySelectorAll('[data-time]')){{
  button.addEventListener('click',()=>{{video.pause();video.currentTime=Number(button.dataset.time);}});
}}
document.querySelector('select').addEventListener('change',event=>{{video.playbackRate=Number(event.target.value);}});
</script></html>''', encoding="utf-8")


def inspect_video(path, contact_path, times=None, columns=2, save_frames=False, preview_width=None):
    """Sample the frame displayed at each time, using decoded presentation times.

    Times are seconds from the first decoded frame. The duration endpoint selects
    the last frame. Decode the whole video while retaining only requested images.
    """
    path, contact_path = Path(path), Path(contact_path)
    if columns < 1:
        raise ValueError("columns must be positive")
    if preview_width is not None and (not isinstance(preview_width, int) or preview_width < 160):
        raise ValueError("preview_width must be an integer of at least 160 pixels")
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
    preview_height = round(preview_width * height / width) if preview_width else 360
    tile_width, tile_height = preview_width or 640, preview_height + 30
    sheet = Image.new("RGB", (tile_width * columns, tile_height * math.ceil(len(samples) / columns)), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for slot, sample in enumerate(samples):
        image = sample.pop("image")
        if save_frames:
            frame_path = contact_path.parent / f"frame-{sample['frame_index']:06d}.png"
            image.save(frame_path)
            sample["frame_path"] = str(frame_path.resolve())
        if preview_width:
            image = image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        else:
            image.thumbnail((640, 360))
        x, y = slot % columns * tile_width, slot // columns * tile_height
        sheet.paste(image, (x + (tile_width - image.width) // 2,
                           y + 30 + (preview_height - image.height) // 2))
        draw.text((x + 8, y + 8),
                  f"want {sample['requested_seconds']:.3f}s | frame {sample['frame_index']} @ {sample['actual_seconds']:.3f}s",
                  fill="black")
    sheet.save(contact_path)
    return {"artifact": str(path.resolve()), "width": width, "height": height, "duration_seconds": duration,
            "decoded_frames": total, "bytes": path.stat().st_size,
            "video_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "contact_sheet": str(contact_path.resolve()), "samples": samples,
            "contact_preview": {"width": tile_width, "height": preview_height,
                                "mode": "exact width" if preview_width else "fit 640x360"},
            "sampling": "displayed frame at requested time (presentation timestamps)",
            "visual_review": "not performed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--at", type=float, action="append", help="Seconds from first frame; repeatable")
    parser.add_argument("--around", type=float, action="append", help="Sample before/at/after a transition; repeatable")
    parser.add_argument("--radius", type=float, default=0.3, help="Seconds on each side of --around (default: 0.3)")
    parser.add_argument("--samples", type=int, default=5, help="Odd sample count per --around (default: 5)")
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--preview-width", type=int,
                        help="Preview each frame at this width, preserving aspect (e.g. 360 for phone viewing)")
    parser.add_argument("--output", type=Path, required=True, help="Directory for contact.png and report.json")
    args = parser.parse_args()
    times = args.at
    if args.around:
        try:
            times = (times or []) + transition_times(args.around, args.radius, args.samples)
        except ValueError as error:
            parser.error(str(error))
    report = inspect_video(args.video, args.output / "contact.png", times, args.columns,
                           save_frames=True, preview_width=args.preview_width)
    review = args.output / "review.html"
    write_review_page(report, review)
    report["review_player"] = str(review.resolve())
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
