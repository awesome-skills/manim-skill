#!/usr/bin/env python3
"""Render runnable examples and record media evidence; not a visual-approval test."""
import argparse
import ast
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys

import av

if __package__:
    from .video_inspection import inspect_video
else:
    from video_inspection import inspect_video

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-tex", action="store_true", help="Requires working LaTeX/dvisvgm")
    parser.add_argument("--include-typst", action="store_true", help="Requires manim[typst]")
    parser.add_argument("--scene", action="append", help="Only these scene names; repeatable")
    parser.add_argument("--output", type=Path, default=ROOT / "verification")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {"manim_version": importlib.metadata.version("manim"),
              "python": sys.version, "renderer": "cairo", "visual_review": "not performed",
              "results": [], "skipped": []}
    selected = set(args.scene or [])
    found = set()
    for source in sorted((ROOT / "examples").glob("*.py")):
        tree = ast.parse(source.read_text())
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if not any(isinstance(base, ast.Name) and base.id.endswith("Scene") for base in node.bases):
                continue
            name = node.name
            if selected and name not in selected:
                continue
            found.add(name)
            reason = None
            if name == "MathExample" and not args.include_tex:
                reason = "optional TeX backend not requested"
            if name in {"TypstFormula", "TypstDerivation"} and not args.include_typst:
                reason = "optional Typst backend not requested"
            if reason:
                report["skipped"].append({"scene": name, "reason": reason})
                continue
            scene_dir = output / name
            scene_dir.mkdir(exist_ok=True)
            command = [sys.executable, "-m", "manim", "render", "-ql", "--renderer", "cairo",
                       "--format", "mp4", "--resolution", "640,360", "--fps", "15",
                       "--disable_caching", "--media_dir", str(scene_dir), str(source), name]
            result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            (scene_dir / "render.log").write_text(result.stdout)
            entry = {"scene": name, "source": str(source.relative_to(ROOT)),
                     "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                     "command": command, "exit_code": result.returncode, "status": "failed"}
            if result.returncode == 0:
                videos = list(scene_dir.glob(f"videos/**/{name}.mp4"))
                if len(videos) == 1:
                    try:
                        entry.update(inspect_video(videos[0], scene_dir / "contact.png"))
                        if (entry["width"], entry["height"]) != (640, 360):
                            raise ValueError("Unexpected output dimensions")
                        entry.update(status="passed", artifact=str(videos[0]))
                    except (ValueError, av.error.FFmpegError) as error:
                        entry["error"] = str(error)
                else:
                    entry["error"] = f"Expected one final video, found {len(videos)}"
            report["results"].append(entry)
            print(f"{name}: {entry['status']}", flush=True)
    unknown = selected - found
    if unknown:
        report["unknown_scenes"] = sorted(unknown)
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Report: {output / 'report.json'}")
    return int(bool(unknown) or not report["results"] or any(r["status"] != "passed" for r in report["results"]))


if __name__ == "__main__":
    raise SystemExit(main())
