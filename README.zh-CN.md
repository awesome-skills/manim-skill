# Manim Skill

让 AI 编程 Agent 使用 **Manim Community Edition** 制作解释性动画。输入要讲的概念，skill 引导 Agent 编写场景、低清预览、检查画面，再交付成品与可编辑源码。

[English](README.md) · [Skill 指令](SKILL.md) · [Manim 0.22 文档](https://docs.manim.community/en/v0.22.0/)

## 适用范围

数学讲解、算法动画、动态技术图解、视频和 GIF。普通静态图表或交互网页无需默认使用 Manim。当前适配 **ManimCE 0.22.x、Python 3.11+**；已有项目保留原来的引擎和版本约束，不自动迁移。

## 安装 skill

```bash
git clone https://github.com/awesome-skills/manim-skill.git
```

把包含 `SKILL.md`、`references/`、`examples/` 和 `scripts/` 的仓库目录安装到 Agent 的 skills 路径。Codex 可以使用 `~/.codex/skills/manim-skill/`；其他能读取 Markdown 的 Agent 也可使用。如果已有统一 skills 目录，沿用现有软链接架构。

安装 skill 和安装 Manim 渲染环境是两回事。

例如：

> 用 Manim 解释三步校验流程，生成可读的 10 秒 MP4。先低清渲染并检查中间状态，再交付 Python 源码和最终视频。

## 安装渲染环境

先按[官方说明](https://docs.manim.community/en/stable/installation.html)准备当前系统的原生依赖，再在仓库中执行：

```bash
uv sync --python 3.13 --extra typst
uv run python -m manim --version
uv run python -m manim checkhealth
uv run python -m manim render -ql examples/basic_scene.py BasicScene
```

`pyproject.toml` 限制 Manim 为 `>=0.22,<0.23`，`uv.lock` 锁定具体依赖以便复现。不需要 Typst 时可省略 `--extra typst`。`MathExample` 需要外部 TeX 工具链；其余基础示例使用 Pango 文字。

普通编码由 PyAV 处理，不要求单独安装 FFmpeg 可执行程序；Cairo/Pango、字体等依赖仍然存在。ManimCE 与 ManimGL 是不同引擎，API 不能混用。

## 示例

| 文件 | 内容 |
|---|---|
| `examples/basic_scene.py` | 基础图形、代码高亮、可选 TeX 公式、无 TeX 曲线图 |
| `examples/flowchart.py` | 线性流程、分支、步骤高亮 |
| `examples/state_diagram.py` | 状态转换、位置索引错配、循环 |
| `examples/quicksort.py` | 真实 Lomuto 事件；交换时移动原柱子与数字 |
| `examples/typst_scene.py` | 无需 TeX 发行版的可选公式示例 |
| `examples/typst_derivation.py` | 可选 Typst 推导：显式区分重复项，固定等号，展示两边减项与消去 |
| `examples/advanced_scene.py` | Cairo 相机聚焦和 3D 环绕 |
| `examples/visual_story.py` | 原创向量首尾相接示例：坐标输入、连续平移与数值结果，无需 TeX |
| `examples/merge_step.py` | 浅色归并解释：稳定卡片身份、相等值取左、清晰运动通道 |
| `examples/wave_superposition.py` | 深色波形叠加：一个相位同时驱动输入与结果 |
| `examples/interference_study.py` | 视觉精修：编辑式版面、等比例波形与突出显示的结果振幅 |
| `examples/data_to_decision.py` | 同一批记录连续变成分组计数柱，并检查小屏可读性 |
| `examples/area_scale_story.py` | 动态大字与几何证明：边长翻倍，四块单位面积填满新正方形 |
| `examples/local_linearity.py` | 镜头聚焦与局部/整体比较：几何保持，字幕按当前视野调整 |
| `examples/circle_to_wave.py` | 连续转场：保留同一个运动点，从圆周运动衔接到正弦轨迹 |
| `examples/damping_story.py` | 三段阻尼讲解：保持初始条件，解析运动与能量同步 |
| `examples/bezier_construction.py` | 几何曲线设计：两级线性插值构造二次 Bézier 轨迹 |
| `examples/exploded_layers.py` | 三维分解视图：保持部件尺寸，按镜头投影安排屏幕文字 |
| `examples/motion_timing.py` | 横竖屏节奏对照：共享线性时钟，以等时间标记显示缓动差异 |
| `examples/packet_journey.py` | 请求的因果流程：分别为横屏和竖屏组织构图 |

快速排序是较长的展示示例，不是所有博客动画的默认时长。短视频应减少输入规模或聚焦一个步骤。

## 输出

```bash
uv run python -m manim render -qh --format mp4 examples/basic_scene.py BasicScene
uv run python -m manim render -qm --format gif examples/basic_scene.py BasicScene
uv run python -m manim render -ql --format png examples/basic_scene.py BasicScene
uv run python -m manim render -ql examples/typst_scene.py TypstFormula
```

`png` 只保存最后一帧。需要打开生成文件时加 `-p`；0.22 的 `-p` 与 OpenGL 实时窗口不同。旧命令和配置时机的变化见[迁移说明](references/setup-and-migration.md)。

## 开发与验证

```bash
uv sync --locked --extra typst
uv run python -m unittest discover -s tests -v
uv run python scripts/smoke.py --include-typst
# 已安装 TeX 时：
uv run python scripts/smoke.py --include-tex --include-typst
# 只检查指定场景：
uv run python scripts/smoke.py --scene BasicScene --scene CodeExample
```

无需重渲染，检查已有 MP4 的指定过渡时刻（替换文件名和秒数）：

```bash
uv run python scripts/video_inspection.py scene.mp4 --at 6.8 --at 8 --columns 2 --output verification/review
# 检查过渡前后，并打开 verification/transition/review.html：
uv run python scripts/video_inspection.py scene.mp4 --around 4.2 --radius 0.3 --samples 5 --output verification/transition
```

检查器保存原分辨率 PNG、多行拼图，以及包含实际呈现时间与输入哈希的 JSON。它按请求时刻正在显示的帧采样，支持不规则帧间隔，并解码全片。时间从首帧算起，时长端点选择末帧；工具不判断美观或播放效果。

CLI 还会生成本地 `review.html`，提供时间点跳转和播放速度选择。保持视频原来的相对路径即可打开；浏览器跳转用于观看，精确帧证据仍以 PNG/JSON 为准。`--around` 检查过渡前后，`--samples` 为至少 3 的奇数，越界时报错。视频不上传，也不增加运行时依赖。

竖屏示例：`uv run python -m manim render -qm --resolution 720,1280 examples/packet_journey.py PacketJourney`。这个场景在构造相机前设置匹配的场景尺寸，并把路线改为竖排；只改像素尺寸不能自动适配任意场景。 `MotionTiming` 也适配这一画幅，使用较短轨道与分行文字：把命令末尾替换为 `examples/motion_timing.py MotionTiming`。

检查脚本为选中的场景生成 640×360、15 fps 的 Cairo MP4，解码全部帧、检查分辨率和正时长，并输出日志、关键帧拼图和 `verification/report.json`。报告记录 Python/Manim 版本、源码哈希、命令、失败及可选后端跳过原因。生成文件不进入 Git；比较不同运行时请使用不同输出目录。

**渲染成功不等于视觉验收。** 拼图用于检查裁切、遮挡、缺字和状态错误；播放视频才能判断节奏和连续性。报告中的 `visual_review` 保持 `not performed`，实际人工检查结果另外记录。测试还检查算法的身份与顺序、几何和物理关系、竖屏相机尺寸，以及真实编码视频上的时间采样、不规则呈现时间和 CLI 输出。

CI 在 Python 3.11 和 3.13 上渲染普通示例及 Typst 示例，并在 3.13 中安装 TeX 验证 `MathExample`，保存运行证据。OpenGL 和平台字体需分别验证，不能用 Cairo 的通过结果代替。

## 按需参考

- [视觉精修方法](references/aesthetic-refinement.md)：美术方向、字体、留白与动作细节；[精修前后对比](docs/evaluations/art-direction-20261029/review.md)。
- [视觉导演](references/visual-direction.md)：镜头设计、视觉层次、运动编排与视觉迭代，附一手研究参考。
- [动画创作配方](references/animation-recipes.md)：视觉风格、对象身份、连续状态、因果流程、节奏与竖屏构图。

- [安装与迁移](references/setup-and-migration.md)
- [图形对象、文字与布局](references/mobjects.md)
- [动画、对象身份与时序](references/animations.md)
- [相机、3D 与排错](references/advanced.md)
- [叙事与博客模式](references/blog-patterns.md)

只读取当前任务需要的参考。完整场景以可执行示例为准，文档不再重复维护同一份示例代码。

[项目调研与采用取舍](docs/research/animation-projects-2026-10-26.md)记录了这轮调研采用或暂缓的方向。另见[公式机制调研](docs/research/formula-and-preview-projects-2026-10-26.md)与[预览反馈调研](docs/research/preview-feedback-projects-2026-10-26.md)。

[渲染反馈评估调研](docs/research/render-feedback-evaluation-2026-10-26.md)与[新会话最大堆试用](docs/evaluations/heap-repair-20261026/review.md)记录具体生成结果，并保留尚未测量的普遍效果。

[30 个动画项目调研](docs/research/animation-craft-2026-10-29.md)记录本轮来源与融合落点；[验收记录](docs/evaluations/animation-craft-20261029/review.md)区分可运行机制、画面采样和未测量的普遍审美/教学效果。

[2026-10-30 本地回归](docs/evaluations/full-craft-regression-20261030/report.json)完成 28 个场景的渲染和解码，包含 Typst；可选 TeX 场景跳过。结果覆盖记录中的本地 Cairo 环境，不代表普遍视觉验收。

## 查看具体改进

以下记录包含源码快照和前后对比采样帧，用来检验具体变化，不代表普遍审美评测，也不保证每次生成都能达到同样效果。

| 机制 | 对照记录 |
|---|---|
| 小屏波形的文字与层次 | [干涉波形精修](docs/evaluations/interference-phone-20261029/review.md) |
| 排序中的对象身份 | [相等值归并](docs/evaluations/merge-stability-20261030/review.md)、[快速排序真实换位](docs/evaluations/quicksort-craft-20261030/review.md) |
| 有信息增量的几何结论 | [向量坐标结果](docs/evaluations/vector-craft-20261030/review.md)、[面积缩放](docs/evaluations/continuous-craft-20261029/review.md) |
| 连续转场与三维构图 | [圆周到波形](docs/evaluations/continuous-transition-20261029/review.md)、[分层分解](docs/evaluations/three-d-craft-20261029/review.md) |
| 新题材生成与仍存差距 | [光圈首轮和修订](docs/evaluations/aperture-forward-20261029/review.md) |

[来源与许可核查](docs/research/source-evidence-audit-2026-10-30.md)记录已检查的上游许可文件，以及原始研究响应归档到本地忽略目录的处理。

## 许可

MIT，见 [LICENSE](LICENSE)。
