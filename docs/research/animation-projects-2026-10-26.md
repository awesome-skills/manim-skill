# 解释动画项目调研：保留 CE，吸收创作机制

调研日期：2026-10-26。目标是提高解释动画的表达与迭代质量，同时控制 skill 的维护范围。
结论：采用“语义节拍 + 局部迭代 + 对象对应”的方法；保留 ManimCE，旁白与演示插件按真实交付需求引入。

## 证据边界与版本

- 已阅读本仓库 `references/visual-direction.md`、`examples/visual_story.py` 与现有工作流；下文对它们的描述来自源码。
- 上游机制来自官方文档、官方仓库源码；未安装或运行下列外部项目，未播放其成片。
- 因此，“可借鉴”属于机制与维护成本判断；本报告没有证明某种配色、运镜或节奏必然更美。
- 用 `gh api repos/OWNER/REPO` 查询默认分支，再用 `gh api repos/OWNER/REPO/commits/HEAD` 取得下表 SHA；链接固定到该快照。
- 默认分支源码不等于 PyPI/npm 已发布版本；依赖声明也不等于与本项目 CE 0.22 环境完成集成测试。

| 项目 | 默认分支 | 2026-10-26 查询所得提交 | 仓库许可标识 |
|---|---|---|---|
| 3b1b/manim | master | `fafa083a4fb274bba9cabde0b6e2f50ba6da0622` | MIT |
| 3b1b/videos | master | `306a1346a356c7a7b097875ceb51c5cd67d0a56c` | README：CC BY-NC-SA 4.0；GitHub API：NOASSERTION |
| motion-canvas/motion-canvas | main | `7b91435c301d530351dcf5ebb91dd139c002e405` | MIT |
| ManimCommunity/manim-voiceover | main | `3dc0d95d2f1d9d0937872b3dd68c7b38c4dfc96a` | MIT |
| jeertmans/manim-slides | main | `df0f1f18f799cd38de0712b0abc4507d4d94b822` | MIT |

许可仅转录仓库标识；具体材料的使用仍应查对应文件与条款，不作法律结论。

## 3b1b/manim：学习变换的语义，不增加第二套运行时

- 机制：`OpeningManimExample` 直接变换坐标网格；`TexTransformExample` 用显式匹配项维持公式对应；`GraphExample` 将点绑定到 tracker；`InteractiveDevelopment` 提供 `embed()`。
  证据：[example_scenes.py][gl-examples]。
- 用户价值判断：同一个对象跨表示保持可追踪，几何动作可以承担解释；局部试验可减少整条时间线的返工。
- 代价：例子使用 `manimlib`，匹配公式、camera 与交互 API 与 CE 不同；照搬将增加第二引擎、环境与验证分支。
  证据：[示例导入与实现][gl-examples]、[官方 workflow 的引擎差异提醒][videos-readme]。
- 许可：[LICENSE.md][gl-license] 标为 MIT；这不覆盖下一个视频内容仓库。
- 决策：**采用创作原则，暂缓引擎引入**。本仓库已有 CE 对象变换、tracker 与局部低清预览，优先把它们用于解释。

## 3b1b/videos：研究注意力组织，保持内容许可边界

- 机制：README 的 `-se` 定位与 `checkpoint_paste()` 可以从注释命名的保存状态重复试验，支持 skip/record；这是作者的 ManimGL + 编辑器工作流。
  证据：[Workflow][videos-readme]。
- 场景证据：`ForcedOscillatorEquation` 将同一框依次移向力项、频率；`MoveAroundPolesSeeDynamics` 使用 trackers、固定在画面的图像与 camera 重定向。
  证据：[derivatives.py][videos-derivatives]。这只能确认代码中的注意力切换与联动机制，不能确认最终镜头观感。
- 用户价值判断：先让观众看见局部关系，再回到整体后果；改一个困难镜头时保持已建立的上下文。
- 代价：README 明确旧项目可能依赖旧版 Manim、无法直接运行；复现完整工作流还涉及定制编辑器插件及场景依赖。
  证据：[README][videos-readme]。
- 许可：README 明确内容为 **CC BY-NC-SA 4.0**，而 Manim 引擎为 MIT；不能把视频代码或资产纳入本仓库 MIT 示例。
  证据：[许可声明][videos-readme]。
- 决策：**采用源码研究与原创重实现，拒绝打包上游视频代码/资产**。当前 VectorStory 为独立 CE 示例；本报告没有执行逐字相似性审计。

## Motion Canvas：有价值的是可编辑节拍与依赖联动

- 机制一：TypeScript generators 描述动画，`all`、`chain`、`sequence` 等组织并行、串行与错峰；编辑器提供实时预览。
  证据：[README][mc-readme]、[Animation flow][mc-flow]。
- 机制二：`waitUntil('event')` 使用命名事件；编辑器拖动时间事件可同时调整后续事件，`useDuration` 可读取时长。
  证据：[Time Events][mc-time]。它明确针对配音改动后硬编码延时需要逐处修改的问题。
- 机制三：signals 将一个可变值的变化传播到依赖它的属性；适合使图、标签与读数来自同一参数。
  证据：[Signals][mc-signals]。
- 用户价值判断：事件名称保留“什么时候、为什么发生”的语义；依赖联动使数值、位置与说明更容易保持一致。
- 代价：完整采用要维护 TypeScript、Vite、浏览器编辑/渲染与另一套节点 API；现有 Python/CE 示例不能直接沿用。
  证据：[包结构、编辑器与 Vite 工作流][mc-readme]。这是集成范围判断，不是性能比较。
- 许可：[LICENSE][mc-license] 标为 MIT。
- 决策：**采用命名节拍的作者习惯，暂缓运行时**。CE sections 可以命名片段，但并不提供 Motion Canvas 的拖动时间线或音频同步。

## manim-voiceover：有旁白时再引入真实时长与书签

- 机制：`voiceover(...)` 上下文返回 tracker；退出时等待剩余音频；`get_remaining_duration()` 与 `wait_until_bookmark()` 将动作接到声音时间上。
  证据：[voiceover_scene.py][vo-scene]、[tracker.py][vo-tracker]。
- 精度边界：书签由文本偏移和词边界插值得到；词边界不足时使用线性 fallback；没有词边界数据时书签检查报错。
  证据：[tracker.py][vo-tracker]。因此不能承诺任意服务、语言或录音都有准确逐词同步。
- 用户价值判断：真实旁白长度变化后，动作可以继续跟随语句；适合录制讲解与需要声音提示的演示。
- 代价：快照声明 Python >=3.11，基础依赖包括 sox、pydub、mutagen 等；录音、转写、各 TTS 服务另有 extras。
  证据：[pyproject.toml][vo-project]。服务账号、费用、录音设备与对齐质量需要按选用路径核查；本次未测。
- 许可：[LICENSE][vo-license] 标为 MIT；语音服务与生成内容的条件需另查。
- 决策：**暂缓依赖引入，保留按需入口**。真实用户要求旁白时，先在当前 CE 环境完成短片段兼容性与中文对齐验证；静音示例无需承担它的依赖。

## manim-slides：解决现场控制，不直接解决画面质量

- 机制：`Slide` 替代 `Scene`，`next_slide()` 切分；`next_slide(loop=True)` 使后续片段循环，等待演讲者继续。
  证据：[README 用法][slides-readme]。
- 用户价值判断：讲师可以在一个状态停留、回应问题，并反复展示运动；适合课堂与现场演示。
- 代价：改变场景基类与交付方式；基础依赖含 qtpy、Jinja2、python-pptx 等，Qt 绑定另列 extras；HTML 与桌面演示需要各自验收。
  证据：[pyproject.toml][slides-project]。`manim>=0.19` 是声明范围，不是本仓库 CE 0.22 的运行证明。
- 许可：[LICENSE.md][slides-license] 标为 MIT。
- 决策：**暂缓默认引入**。用户明确要可控演示/HTML slides 时再走这条分支；普通 MP4 的构图与节奏问题仍由场景设计解决。

## 本次采用的最小补充

- 已在 `references/visual-direction.md` 加入 **Editable timing**；`VectorStory` 已命名 `same_origin`、`head_to_tail`、`resultant` 三个 CE section。
- 这项补充吸收 Motion Canvas 的语义事件思路，把一个动作与它的停留放在一起，便于局部改动；没有新增第三方依赖。
- 维护成本仍包括三处名称、片段边界和可选导出检查；它没有实现声音提示驱动，也不会自动修正旁白变化。
- CE 官方 `next_section` 创建片段边界；`--save_sections` 才要求生成分段视频及相关元数据。
  证据：[CE v0.22.0 Scene 源码][ce-scene]、[v0.22.0 输出教程源码][ce-sections]。
- 实际导出、逐帧解码、采样帧检查和全速播放是独立验收；本调研未执行这些操作，结果由实现任务的当前证据给出。
- 本次不扩展第六个项目：现有来源已覆盖对象对应、局部迭代、时序、旁白、演示五类实际需求。

## 固定来源

[gl-examples]: https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/example_scenes.py
[gl-license]: https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/LICENSE.md
[videos-readme]: https://github.com/3b1b/videos/blob/306a1346a356c7a7b097875ceb51c5cd67d0a56c/README.md
[videos-derivatives]: https://github.com/3b1b/videos/blob/306a1346a356c7a7b097875ceb51c5cd67d0a56c/_2025/laplace/derivatives.py
[mc-readme]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/README.md
[mc-flow]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/docs/docs/getting-started/flow.mdx
[mc-time]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/docs/docs/getting-started/time-events.mdx
[mc-signals]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/docs/docs/getting-started/signals.mdx
[mc-license]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/LICENSE
[vo-scene]: https://github.com/ManimCommunity/manim-voiceover/blob/3dc0d95d2f1d9d0937872b3dd68c7b38c4dfc96a/src/manim_voiceover/voiceover_scene.py
[vo-tracker]: https://github.com/ManimCommunity/manim-voiceover/blob/3dc0d95d2f1d9d0937872b3dd68c7b38c4dfc96a/src/manim_voiceover/tracker.py
[vo-project]: https://github.com/ManimCommunity/manim-voiceover/blob/3dc0d95d2f1d9d0937872b3dd68c7b38c4dfc96a/pyproject.toml
[vo-license]: https://github.com/ManimCommunity/manim-voiceover/blob/3dc0d95d2f1d9d0937872b3dd68c7b38c4dfc96a/LICENSE
[slides-readme]: https://github.com/jeertmans/manim-slides/blob/df0f1f18f799cd38de0712b0abc4507d4d94b822/README.md
[slides-project]: https://github.com/jeertmans/manim-slides/blob/df0f1f18f799cd38de0712b0abc4507d4d94b822/pyproject.toml
[slides-license]: https://github.com/jeertmans/manim-slides/blob/df0f1f18f799cd38de0712b0abc4507d4d94b822/LICENSE.md
[ce-scene]: https://github.com/ManimCommunity/manim/blob/v0.22.0/manim/scene/scene.py
[ce-sections]: https://github.com/ManimCommunity/manim/blob/v0.22.0/docs/source/tutorials/output_and_config.rst
