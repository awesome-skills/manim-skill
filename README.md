<p align="center">
  <img src="./assets/banner.svg" alt="Manim Skill Banner" width="100%" />
</p>

<div align="center">

<h3>AI-powered technical animation with ManimCE</h3>

<p>
  <a href="https://github.com/awesome-skills/manim-skill/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-22c55e?style=flat-square" alt="License: MIT"/>
  </a>
  <img src="https://img.shields.io/badge/Manim-Community%20Edition-58b86b?style=flat-square&logo=python&logoColor=white" alt="ManimCE"/>
  <img src="https://img.shields.io/badge/Skill-Agent%20Agnostic-0ea5e9?style=flat-square" alt="Agent Agnostic"/>
  <img src="https://img.shields.io/badge/Lines-3%2C100%2B-7c3aed?style=flat-square" alt="3100+ lines"/>
  <img src="https://img.shields.io/badge/Format-SKILL.md-f59e0b?style=flat-square" alt="SKILL.md"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-ec4899?style=flat-square" alt="PRs Welcome"/>
</p>

<p>
  English &middot; <a href="./README.zh-CN.md">&#31616;&#20307;&#20013;&#25991;</a>
</p>

</div>

---

## What is this?

**manim-skill** is a reusable skill package for creating technical animations with [ManimCE](https://www.manim.community/). It works as a **Codex native skill** and as an **agent-agnostic playbook** for any AI coding assistant that reads markdown.

You describe the animation you want. The agent handles the rest &mdash; pattern selection, code generation, rendering, troubleshooting, and iteration.

---

## &#9889; Agent Capabilities

When provided with `SKILL.md` and relevant `references/` docs, AI agents can autonomously:

| Step | What the agent does |
|------|---------------------|
| **1. Pattern selection** | Choose the right animation type (bars, graphs, diagrams, 3D, camera moves) |
| **2. Code generation** | Write correct ManimCE scene code from your description |
| **3. Rendering** | Execute render commands with appropriate quality flags |
| **4. Troubleshooting** | Fix FFmpeg, TeX, font, and environment issues automatically |
| **5. Iteration** | Refine timing, colors, and layout until the output matches your intent |

---

## &#127912; Supported Agents & IDEs

<p>
  <img src="https://img.shields.io/badge/Claude%20Code-Supported-111827?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Cursor-Supported-111827?style=flat-square&logo=cursor&logoColor=white" alt="Cursor" />
  <img src="https://img.shields.io/badge/Codex%20CLI-Supported-111927?style=flat-square&logo=openai&logoColor=white" alt="Codex CLI" />
  <img src="https://img.shields.io/badge/Gemini%20CLI-Supported-111827?style=flat-square&logo=google&logoColor=white" alt="Gemini CLI" />
  <img src="https://img.shields.io/badge/Qwen%20Code-Supported-111827?style=flat-square&logo=alibabacloud&logoColor=white" alt="Qwen Code" />
  <img src="https://img.shields.io/badge/Cline-Supported-111827?style=flat-square&logo=visualstudiocode&logoColor=white" alt="Cline" />
</p>

| Agent / IDE | How to use |
|---|---|
| **Codex** | Install as a native skill folder (`~/.codex/skills/...`) |
| **Claude Code / Cursor / Cline** | Use `SKILL.md` + `references/` as project instructions or prompt context |
| **Other agents** | Use this repository as a structured Manim playbook |

---

## &#128293; Quick Start

### Install

<details>
<summary><strong>Option 1: Codex native skill</strong></summary>

```bash
# macOS / Linux
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo awesome-skills/manim-skill \
  --path . \
  --name manim-skill
```

```powershell
# Windows PowerShell
python $HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo awesome-skills/manim-skill `
  --path . `
  --name manim-skill
```

</details>

<details>
<summary><strong>Option 2: Standalone playbook</strong></summary>

```bash
git clone https://github.com/awesome-skills/manim-skill.git
cd manim-skill
```

Then feed `SKILL.md` and relevant `references/` files into your agent workflow.

</details>

### Render

```bash
# Fast preview (480p)
uv run --with manim manim -pql examples/quicksort.py QuickSortBars

# GIF export (720p)
uv run --with manim manim -qm --format=gif examples/quicksort.py QuickSortBars

# 4K showcase (2160p60)
manim -qk examples/quicksort.py QuickSortBars
```

---

## &#127916; Preview

<p align="center">
  <video src="./assets/quicksort-preview.mp4" controls muted loop playsinline width="88%">
    Your browser does not support the video tag.
  </video>
</p>

<p align="center">
  <a href="./assets/quicksort-preview.mp4">&#9654;&#65039; Download preview video</a> &middot;
  <a href="./assets/quicksort-preview.png">&#128247; Static fallback image</a>
</p>

---

## &#128218; Content Overview

| File | Lines | Description |
|------|-------|-------------|
| **SKILL.md** | ~380 | Core instructions &mdash; loaded on skill activation |
| **references/mobjects.md** | ~860 | Mobject types, positioning, styling, grouping |
| **references/animations.md** | ~620 | Animation classes, timing, chaining, transforms |
| **references/advanced.md** | ~890 | 3D scenes, camera, ValueTracker, updaters, custom anims |
| **references/blog-patterns.md** | ~410 | Blog-ready patterns: hero banners, step-by-step, comparisons |

**Total: 3,100+ lines** of ManimCE guidance, loaded progressively per topic.

---

## &#128196; Examples

| File | What it demonstrates |
|------|---------------------|
| `examples/basic_scene.py` | Minimal scene setup, shapes, text, basic animations |
| `examples/quicksort.py` | Algorithm visualization with bar charts and step labels |
| `examples/flowchart.py` | Flowchart construction with arrows and styled boxes |
| `examples/state_diagram.py` | State machine with transitions and highlighting |

---

## &#128193; Repository Structure

```
manim-skill/
|
+-- SKILL.md                     # Core skill instructions (~380 lines)
+-- README.md                    # English documentation
+-- README.zh-CN.md              # Chinese documentation
|
+-- examples/                    # Ready-to-run animation scenes
|   +-- basic_scene.py           # Minimal hello-world scene
|   +-- quicksort.py             # Algorithm bar chart animation
|   +-- flowchart.py             # Flowchart with arrows and boxes
|   +-- state_diagram.py         # State machine visualization
|
+-- references/                  # Progressive reference guides
|   +-- mobjects.md              # Shapes, text, tables, graphs, grouping
|   +-- animations.md            # Create, Transform, Fade, timing control
|   +-- advanced.md              # 3D, camera, ValueTracker, updaters
|   +-- blog-patterns.md         # Blog-ready animation recipes
|
+-- assets/                      # Media assets
    +-- banner.svg               # Repository banner
    +-- quicksort-preview.mp4    # Preview video
    +-- quicksort-preview.png    # Static fallback image
```

---

## &#10024; Key Highlights

- **ManimCE v0.19+** &mdash; No external FFmpeg needed (uses pyav internally)
- **Progressive loading** &mdash; Only load the reference docs relevant to your task
- **Windows-friendly** &mdash; PowerShell setup, `uv run` one-liners, font fallback tips
- **TeX-free fallback** &mdash; Numeric labels and `Text()` alternatives when LaTeX is unavailable
- **Production-ready** &mdash; Quality presets from 480p preview to 4K60 showcase

---

## &#129309; Contributing

Contributions are welcome! Priority areas:

- New algorithm animation templates
- Better cross-platform troubleshooting
- More agent integration examples
- Framework-specific patterns (D3-style, Matplotlib-style)
- Translations

---

## &#128196; License

MIT &copy; [awesome-skills](https://github.com/awesome-skills)
