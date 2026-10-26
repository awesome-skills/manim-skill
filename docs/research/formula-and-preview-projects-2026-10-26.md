# 公式变换与快速反馈：第二批调研

2026-10-26；仅阅读官方仓库源码与文档，未安装候选项目、播放成片或运行性能比较。
建议：优先用现有 CE 0.22 `MathTypst` 的标签选择，实现一个明确展示项的来源、复制与去向的推导。
目标是让观众看懂数学操作；字形连续变形与成功渲染都不足以证明推导正确或视觉清楚。

## 快照与本地基线

用 `gh api repos/OWNER/REPO` 和 `gh api repos/OWNER/REPO/commits/HEAD` 查询默认分支及提交；以下链接固定到所查 SHA。
这些日期是分支提交记录，不表示最新包版本、维护承诺或兼容性验证。

| 项目 | 默认分支 / 提交 | 提交日期 UTC | 许可原文标识 |
|---|---|---|---|
| reactive-manim | main / `fa5673ce3cd35615bc83d03976771c53137dfdb4` | 2026-08-31 | MIT |
| instavm/manim-studio | main / `f38a605013ceb551d91bcce6af829ceee1c0c3c7` | 2026-06-16 | MIT |
| ViCo-Lab/candy | main / `0194ef4c36ced8a7f8590a0d3329745f712177ac` | 2026-08-20 | MIT OR Apache-2.0 |
| manim-storytelling-skills | master / `5c6f65d0cec533e3e51c689f1cfa246238a0ee5d` | 2026-08-08 | MIT |

许可来自下方 LICENSE、README 或 manifest；仅转录，不作法律结论。四个仓库查询时均未标记 archived。
本地 `pyproject.toml` 已声明 CE `>=0.22,<0.23` 和可选 `manim[typst]`；调研开始时的 basic/typst 公式示例仅展示公式，尚未展示项的语义推导。

## CE 已经提供什么

- `MathTypst("{{ a : factor }} ...")` 支持命名捕获，`select("factor")` 返回所选 SVG 子对象的 `VGroup`；同形重复项可以使用不同标签。
  实现用保持排版的 `hide` probes 映射叶片；标签选择与字形外观匹配是不同机制。[CE Typst 源码][ce-typst]
- `TransformMatchingTex` 以 `tex_string` 为 key，把同 key 的所有子对象合成组；`key_map` 改的是 key 对应关系，不能单独表达同 key 第一次与第二次出现的身份。
  `TransformMatchingShapes` 则匹配归一化点坐标的 hash；两者都没有数学等价验证。[CE matching 源码][ce-matching]
- 因而简单、唯一项的 LaTeX 重排适合 `TransformMatchingTex`；重复项、展开、合并需作者给出明确分组及对应。
  `MathTypst` 不属于 `MathTexPart`，不能把它直接交给要求该类型的 `TransformMatchingTex`。[CE matching 源码][ce-matching]
- 可用 `ReplacementTransform` 表示一对一去向，用源对象的独立副本/`TransformFromCopy` 表示复制，再显式移除消失项；这是一段场景编排即可完成的工作。[CE transform 源码][ce-transform]
- 排版仍需固定等号或基线、保留字号及间距，检查中途交叉；标签本身不会自动完成这些事。

## reactive-manim：值得借鉴项身份，暂缓引入运行时

- 机制：动态组件有 ID，图状态管理器保存 source/target；`source_id` / `target_id` 决定来源与归宿；`clone()` 分配新 ID 并保留来源 ID。
  这比按字形猜测更接近“同一个项、这个项的副本、被合并的项”。[动态对象实现][reactive-core]
- 布局连续性：`save_y()` / `restore_y()` 保存纵向位置并移动根对象；README 的指数例子利用它维持动作焦点。[源码][reactive-core]、[README][reactive-readme]
- 价值：复杂多步推导可以复用分数、指数等组件，降低逐项布局和身份配对的手写量；它仍不替作者证明运算正确。
- 兼容性证据有界：README 标 CE 0.18.1、要求在 manim 后导入且覆盖 `MathTex`；setup 的版本为 0.0.5，仅声明 `manim>=0.18.1`。
  宽松依赖范围与 README 中 CE 0.21 的媒体文件名均不能证明 CE 0.22 可用。[README][reactive-readme]、[setup.py][reactive-setup]
- 成本：引入组件图、状态生命周期及额外 API；单个教学推导以 CE 标签显式编排更容易核对。
- 许可：[LICENSE][reactive-license] 为 MIT。
- 决策：**采用显式身份/复制/锚点思路，暂缓依赖**；真实需求出现大量复杂推导后，再用小兼容性试验衡量收益。

## instavm/manim-studio：作业反馈可借鉴，云平台不进入 skill

- 源码实际流程：生成代码→InstaVM 渲染→失败时把错误尾部和上次代码发回模型，默认最多 3 次；前端轮询增量日志，成功后提供可播放 MP4。
  这是运行错误修复与交付反馈；所读循环没有把视频帧送回模型评审。[generator.py][studio-generator]、[app.js][studio-ui]
- 价值：用户能看到运行进度、错误以及最终可播放结果；不代表自动发现重叠、错误项对应或节奏问题。
- 边界：README / 渲染安装代码使用 CE 0.20.1；提示词禁止 `Tex/MathTex`，用 Unicode `Text` 绕开 TeX，不能提供公式语义变换能力。[README][studio-readme]、[generator.py][studio-generator]
- 成本：OpenAI 与 InstaVM 凭据、服务运行与远程作业；README 的冷启动时长是项目自述，本次未测。
- 许可：[LICENSE][studio-license] 为 MIT；服务使用成本另计。
- 决策：**采用“错误日志 + 可播放结果”的反馈目标，暂缓平台接入**。现有本地低清 MP4、contact sheet 和报告已覆盖基础反馈；先改善真实画面审查。

## Candy：字形匹配与排版机制可研究，暂缓迁移

- 实际 `transform.rs`：提取完整 Typst 排版中的字形/装饰位置；按 outline signature 及中心距离贪心一对一配对，距离相同用索引稳定排序。
  这能保留 Typst 排版指标，但同形重复项的选择依据是几何邻近，并非代数身份。[transform.rs][candy-transform]
- 因而 `a(b+c) → ab+ac` 的两个目标 `a` 不能仅靠这种一对一配对表达共同来源；同形字母交换角色也可能需要显式规则。这是算法性质推论，未渲染该反例。
- 文档的 reveal/typewriter 为后续内容保留布局盒，避免逐字出现时其余内容跳动；可借鉴为 CE 的固定字幕区域与稳定锚点。[Transforms 文档][candy-doc]
- 快速反馈：CLI 可输出 GIF、PNG、SVG 草稿；PNG 是最后一帧，不能验证运动。源码中的 `preview_demo` 指 Typst `@preview` 包解析示例，并非实时编辑器证据。[CLI][candy-cli]
- 成本与兼容性：这是独立 `.tyx` / Rust 引擎；Cargo 指定 Rust >=1.85、Typst 0.15.1，不是 CE 的 MathTypst 插件。[README][candy-readme]、[Cargo.toml][candy-cargo]
- 许可：Cargo 为 `MIT OR Apache-2.0`，README 说明可任选；GitHub API 返回 NOASSERTION 不能替代实际声明。[Cargo.toml][candy-cargo]、[README][candy-readme]
- 决策：**采用固定布局与短草稿原则，暂缓引擎**；已有 MathTypst 足以满足本次公式排版，暂未发现必须迁移才能解决的需求。

## 第四项筛查：manim-storytelling-skills

- 有具体参考价值：`followers.py` 原地更新跟随标签/连线；`algebra.py` 只是包装 `TransformMatchingTex`，示例按公式片段拆分。[followers][story-follow]、[algebra][story-algebra]
- 这些是 CE 公共 API 的组合，没有增加重复项身份或一变多映射；requirements 仅写 `manim`，不是 CE 0.22 兼容性证据。[requirements][story-requirements]
- 许可：[LICENSE][story-license] 为 MIT。**采用跟随注释的编排原则，拒绝为这些薄包装增加依赖或导入整套框架**；现有 updater 指导已能表达同样方法。

## 候选示例与本次取舍

一个候选是原创短片 `a(b+c) → ab+ac`：先保持完整公式的 Typst 排版，再给源 a、目标 a₁/a₂、b、c、运算符分别命名。
先强调 a 的作用范围，再用两个独立源副本到目标两项，b/c 保持颜色与明确去向；括号淡出，最后整理为等式。
固定等号或一条基线，分开编排复制与整理，避免一个对象同时受多个动画修改。目标公式先整体排版，标签仅用于选择。
不必新增通用匹配器、符号代数系统或依赖；复用现有 Typst extra 和 smoke 流程，新增一个原创例子及一小段选择规则即可。
验收应包含：末态公式正确、两个 a 的来源清楚、重复项没有错配、中途没有跳动/碰撞；分别记录静帧、中间帧和播放审查。
本次实际先落地 `examples/typst_derivation.py`：从 `a²+b²=c²` 出发，两边同时减去 b²，再消去左边的项。三个 b² 各有独立标签；等号固定，消去线退出后保留项才整理到新位置。它验证一对一映射、重复项角色和消去顺序，未实现上面的分配律复制示例。

本报告的外部项目研究只证明 API 与机制路径；本地渲染及中间帧检查由实现任务另行记录，没有跨引擎性能比较或审美优越性结论。

## 固定来源

[ce-typst]: https://github.com/ManimCommunity/manim/blob/v0.22.0/manim/mobject/text/typst_mobject.py
[ce-matching]: https://github.com/ManimCommunity/manim/blob/v0.22.0/manim/animation/transform_matching_parts.py
[ce-transform]: https://github.com/ManimCommunity/manim/blob/v0.22.0/manim/animation/transform.py
[reactive-core]: https://github.com/philip-murray/reactive-manim/blob/fa5673ce3cd35615bc83d03976771c53137dfdb4/reactive_manim/src/dynamic_mobject.py
[reactive-readme]: https://github.com/philip-murray/reactive-manim/blob/fa5673ce3cd35615bc83d03976771c53137dfdb4/README.md
[reactive-setup]: https://github.com/philip-murray/reactive-manim/blob/fa5673ce3cd35615bc83d03976771c53137dfdb4/setup.py
[reactive-license]: https://github.com/philip-murray/reactive-manim/blob/fa5673ce3cd35615bc83d03976771c53137dfdb4/LICENSE
[studio-generator]: https://github.com/instavm/manim-studio/blob/f38a605013ceb551d91bcce6af829ceee1c0c3c7/manimstudio/generator.py
[studio-ui]: https://github.com/instavm/manim-studio/blob/f38a605013ceb551d91bcce6af829ceee1c0c3c7/manimstudio/static/app.js
[studio-readme]: https://github.com/instavm/manim-studio/blob/f38a605013ceb551d91bcce6af829ceee1c0c3c7/README.md
[studio-license]: https://github.com/instavm/manim-studio/blob/f38a605013ceb551d91bcce6af829ceee1c0c3c7/LICENSE
[candy-transform]: https://github.com/ViCo-Lab/candy/blob/0194ef4c36ced8a7f8590a0d3329745f712177ac/rust/src/renderer/typst/transform.rs
[candy-doc]: https://github.com/ViCo-Lab/candy/blob/0194ef4c36ced8a7f8590a0d3329745f712177ac/docs/tutorial/transforms.md
[candy-cli]: https://github.com/ViCo-Lab/candy/blob/0194ef4c36ced8a7f8590a0d3329745f712177ac/docs/reference/cli.md
[candy-readme]: https://github.com/ViCo-Lab/candy/blob/0194ef4c36ced8a7f8590a0d3329745f712177ac/README.md
[candy-cargo]: https://github.com/ViCo-Lab/candy/blob/0194ef4c36ced8a7f8590a0d3329745f712177ac/rust/Cargo.toml
[story-follow]: https://github.com/dbillion/manim-storytelling-skills/blob/5c6f65d0cec533e3e51c689f1cfa246238a0ee5d/manim-brilliance-explainer/shots/followers.py
[story-algebra]: https://github.com/dbillion/manim-storytelling-skills/blob/5c6f65d0cec533e3e51c689f1cfa246238a0ee5d/manim-brilliance-explainer/shots/algebra.py
[story-requirements]: https://github.com/dbillion/manim-storytelling-skills/blob/5c6f65d0cec533e3e51c689f1cfa246238a0ee5d/manim-brilliance-explainer/requirements.txt
[story-license]: https://github.com/dbillion/manim-storytelling-skills/blob/5c6f65d0cec533e3e51c689f1cfa246238a0ee5d/LICENSE
