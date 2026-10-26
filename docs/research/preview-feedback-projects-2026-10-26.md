# 预览反馈调研：先补指定时间的本地视频检查

2026-10-26。仅检查官方源码与文档，未安装扩展、操作编辑器、播放其演示或做性能测试。
建议：用已有 PyAV/Pillow 增加已生成本地 MP4 的指定时间采样与可读 contact sheet，暂缓编辑器及运行时集成。

## 来源快照与边界

通过 `gh api repos/OWNER/REPO` 与 `gh api repos/OWNER/REPO/commits/HEAD` 取得默认分支和 SHA。
日期是当前默认分支提交记录，不能据此证明已发布版本、维护承诺或在本机的兼容性。

| 项目 | 分支 / SHA | 提交日期 UTC | 许可文件标识 |
|---|---|---|---|
| Rickaym/manim-sideview | master / `49830a7aa69c84b3d1cbad9f37921501b9ee57de` | 2026-09-09 | MIT |
| Manim-Notebook/manim-notebook | main / `398fdf835b5b17f7e1b1d33953056b4326a226c5` | 2025-04-14 | MIT |
| behackl/manim-cue | main / `7637604cc9695949ac009545419806b4774284df` | 2026-09-11 | MIT |

`bhoov/manim-notebook` 查询被重定向到上表组织地址；仓库 `pushed_at` 较新并不代表默认分支提交较新。
三个仓库查询时均未标记 archived；许可仅转录文件，不作法律结论。[Sideview][side-license]、[Notebook][notebook-license]、[Cue][cue-license]

## 现有缺口与 CE 基线

- 调研时本地 [`scripts/smoke.py`](../../scripts/smoke.py) 的 `inspect_video` 解码全片，但仅保留帧索引 0、1/4、1/2、3/4、末帧附近的样本，contact sheet 为单行。
- `stream.frames` 为 0/未知时，其索引集合会缩成 `{0}`；这些采样索引也没有标出实际呈现时间。CLI 只接 scene，不接任意 MP4 或用户指定秒数。
- 全片解码可检查媒体是否能解码，但没有对每帧画面做语义检查；五张缩略图也不能代表运动连续性验收。
- CE 0.22 CLI 的 `-n` 选择动画编号范围；PNG 只保存末帧，`png-sequence` 保存渲染的每帧，不是已生成 MP4 的任意时间检查器。[CLI 源码][ce-cli]
- CE v0.22.0 的 `Manager` 提供 render/play 等生命周期协调，源码没有 Cue 所要求的 `evaluate(capture_timeline=...)` 或 `capture_frame_at(...)`。[Manager 源码][ce-manager]

## Manim Sideview：自动打开媒体，采用目标、暂缓集成

- 实际机制：调用 Manim 进程，完成回调解析实际输出路径或回退路径，再 `playMedia`；webview 加载/重新加载已有视频或图片。
  这是渲染后的媒体预览，不是保留 Python scene 内存状态并交互修改。[sideview.ts][side-source]、[player.ts][side-player]
- 用户价值：少一次寻找并打开输出文件的操作，源代码与预览并排可见；视频仍需用户观看判断。
- 约束：`package.json` 声明 VS Code ^1.68.0 与 Microsoft Python 扩展；实现处理解释器、配置、输出日志和媒体路径，增加宿主集成维护面。[manifest][side-package]
- 决策：**采用生成后容易查看媒体的目标，暂缓扩展接入**。本次需要的是可复用的时间点证据，不需要增加 VS Code 前提；本次未实测其 CE 0.22 兼容性。

## Manim Notebook：交互 checkpoint 有价值，暂缓引擎迁移

- README 明确只支持 ManimGL、不是 CE，也不是 Jupyter；`##` 将 Python 文件分成可执行片段。[README][notebook-readme]
- 源码把选中片段暂存到剪贴板，执行 `checkpoint_paste()`，再恢复剪贴板；reload 路径要求 ManimGL >=1.7.2 并等待 IPython 重启。[previewCode.ts][notebook-source]
- 用户价值：从已有交互场景状态反复试验一小段，而不用每次重新渲染整片；这是局部创作反馈，与检查交付 MP4 的帧是两件事。
- 维护成本：需要 ManimGL 会话、终端/IPython 状态、代码片段边界和 VS Code 行为；对当前 CE skill 引入第二运行时无直接必要。
- 决策：**采用小片段反复迭代的原则，暂缓运行时/编辑器集成**。当前原生 CE sections 和局部低清视频已能支持有边界的迭代。

## Manim Cue：时间点检查值得采用，兼容性依赖实际能力

- 架构分三步：先取得选定时间的静帧，再求执行时间线，最后生成完整预览；每一步运行于新的 Python 进程。[架构][cue-architecture]
- UI 区分选择时间、逐帧、区间循环和播放；视频可用时从视频取帧，否则重跑 scene 捕获。Compare/导出某些路径也会重跑，随机数或外部输入可能让图与视频不同。[用法][cue-usage]
- 源码记录 `requestedTime` 和捕获到的 `frame.time/frame_index`；PyAV probe 使用 `frame.pts * frame.time_base`，没有把平均帧率当作所有呈现时间的替代。[support.py][cue-support]
- 兼容性：README 要求 Manim 预览分支；实际 diagnose 检查 `Manager.capture_frame_at`、`evaluate(capture_timeline)` 与编码配置能力，而非只比较版本号。[README][cue-readme]、[support.py][cue-support]
- 对照 CE v0.22.0 源码，上述两个 Manager 能力未提供；因此当前版本不能直接视为完整兼容。这里是源码对照，未执行扩展能力检测。[Manager][ce-manager]
- 成本：VS Code、Python 扩展、时间线协议、进程/缓存/结果新旧状态等；整套引入显著超过本次 MP4 采样需求。[架构][cue-architecture]
- 决策：**采用时间点导航、实际时间标记和静帧/播放分开的设计，暂缓扩展**。已有视频应直接采样，避免为检查同一成片再次执行 scene。

## 为什么仅靠关键帧或四分点不足

这是采样覆盖范围的推论，不是外部项目的测量结果：任意有限样本之间都有未观察区间，短暂碰撞、错位或消失可以发生在区间内。
即使样本都是有语义的起点/终点，正确端点也不限制中间运动路径；时间四分点同样可能都落在停留段。
Cue 明确分别提供选定静帧、逐帧和区间播放，体现这些观察手段各有用途；源码并未证明任何固定样本集可检出所有问题。[用法][cue-usage]
交换看相遇附近，消去看淡出/划线附近，变形看中间状态；用相邻时间点定位问题，再以原速片段播放判断节奏和连续性。
截图可支持某个实际时间点的布局结论，不能支持“整段运动自然”或音画同步验收。

## 最小实现方向

建议独立本地 CLI：输入 MP4、秒数列表、输出目录、列数；复用 PyAV/Pillow，不运行 scene、不导入编辑器。
采样直接顺序解码同一输入视频，按呈现时间选择请求时刻正在显示的帧（不晚于请求时间的最后一帧）；避免先做关键帧 seek 优化。
秒数以第一张视频帧的 PTS 为零点；使用 `PTS × time_base`，不用 `frame_index / average_rate` 推算。
输出 PNG、按指定列数换行的 contact sheet 和 JSON；每张标注“请求秒数、实际秒数、解码索引”，保持原始宽高比。
默认只留有限请求对应的图像，逐帧更新候选；单次解码时间随视频长度增长。这是明确的简单性取舍，未做性能承诺。
拒绝非有限/负时间、没有可用 PTS 或无视频帧；请求限制在 [0, 视频时长]；时长端点明确选择末帧，超过时长报错。时长和 PTS 元数据不可用时明确报错，不推测时间。
结果保留输入绝对路径和实际时间，明确 `visual_review` 尚未完成；媒体解码、采样布局与播放审查分别记录。
验证范围：已知时间戳短视频的显示帧/不规则时间戳/边界，列数布局和比例，以及真实动画的困难过渡采样；保持测试与这几个契约对应。
本轮将采样器实现为 `scripts/video_inspection.py`，smoke 复用同一函数；CLI 另存原分辨率 PNG，smoke 仅保存拼图以控制 CI 产物体积。报告含输入视频 SHA-256，便于核对同一成片。

这项工作直接消除重复手写采样脚本和超宽单行拼图；播放仍使用现有播放器，本次不建设通用时间线编辑器。

## 固定来源

[side-source]: https://github.com/Rickaym/manim-sideview/blob/49830a7aa69c84b3d1cbad9f37921501b9ee57de/src/sideview.ts
[side-player]: https://github.com/Rickaym/manim-sideview/blob/49830a7aa69c84b3d1cbad9f37921501b9ee57de/src/player.ts
[side-package]: https://github.com/Rickaym/manim-sideview/blob/49830a7aa69c84b3d1cbad9f37921501b9ee57de/package.json
[side-license]: https://github.com/Rickaym/manim-sideview/blob/49830a7aa69c84b3d1cbad9f37921501b9ee57de/LICENSE
[notebook-readme]: https://github.com/Manim-Notebook/manim-notebook/blob/398fdf835b5b17f7e1b1d33953056b4326a226c5/README.md
[notebook-source]: https://github.com/Manim-Notebook/manim-notebook/blob/398fdf835b5b17f7e1b1d33953056b4326a226c5/src/previewCode.ts
[notebook-license]: https://github.com/Manim-Notebook/manim-notebook/blob/398fdf835b5b17f7e1b1d33953056b4326a226c5/LICENSE.txt
[cue-readme]: https://github.com/behackl/manim-cue/blob/7637604cc9695949ac009545419806b4774284df/README.md
[cue-architecture]: https://github.com/behackl/manim-cue/blob/7637604cc9695949ac009545419806b4774284df/docs/architecture.md
[cue-usage]: https://github.com/behackl/manim-cue/blob/7637604cc9695949ac009545419806b4774284df/docs/usage.md
[cue-support]: https://github.com/behackl/manim-cue/blob/7637604cc9695949ac009545419806b4774284df/python/support.py
[cue-license]: https://github.com/behackl/manim-cue/blob/7637604cc9695949ac009545419806b4774284df/LICENSE
[ce-manager]: https://github.com/ManimCommunity/manim/blob/v0.22.0/manim/manager.py
[ce-cli]: https://github.com/ManimCommunity/manim/blob/v0.22.0/manim/cli/render/render_options.py
