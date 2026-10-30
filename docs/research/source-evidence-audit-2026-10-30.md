# 研究来源整理与许可核查

本轮整理研究材料，不修改动画实现或重新渲染。累计筛选数量仍为 61 个不同仓库；数量不代表作品质量或可直接复用的数量。

六份研究 JSON 曾保存完整、部分重复的上游 README 或源码响应。现在把原始响应保存在 Git 忽略的本地目录 `verification/research-source-archive-20261029/`，仓库记录保留来源、SHA-256、字符数及原始 JSON 路径。39 个字段的指纹均与归档核对一致；没有把研究材料改写成原创代码。忽略目录不会随仓库分发，其他读者应通过记录的上游地址查阅，地址内容可能随分支变化。已有 blob SHA 的记录可用于识别当时版本。

2026-10-29 实际读取以下许可文件，结果与文件 blob SHA 见[核查记录](source-evidence-audit-2026-10-30.json)：

| 来源 | 文件核查结果 | 本项目处理 |
| --- | --- | --- |
| [Paper.js](https://github.com/paperjs/paper.js/blob/develop/LICENSE.txt) | MIT | 研究曲线构造；本项目使用原创 Manim 实现 |
| [Pygfx](https://github.com/pygfx/pygfx/blob/main/LICENSE) | BSD-2-Clause | 研究遮挡和透明排序问题；未引入引擎 |
| [VisPy](https://github.com/vispy/vispy/blob/main/LICENSE.txt) | BSD-3-Clause；文件对 examples 另有例外说明 | 仅作技术比较；具体示例仍须检查自身声明 |
| [Animation Nodes](https://github.com/JacquesLucke/animation_nodes/blob/master/license.txt) | GPL-3.0-or-later | 研究节点式组织思路；未移植源码 |
| [typexperiments](https://github.com/pablostanley/typexperiments) | 根目录未找到许可文件，未核实 | 不据此推断可以复制实现或素材 |
| [manim-animations](https://github.com/kelvinleandro/manim-animations) | 根目录未找到许可文件，未核实 | 作为作品研究来源，未移植源码 |

这次核查只覆盖表中的路径，不能代表所有调研项目、字体、图片及依赖均已核实。README 中的许可描述与实际许可文件核查应分开记录。项目自身 MIT 许可不会自动覆盖上游材料。

后续继续以原创示例落实叙事、构图和运动机制；如果需要直接复用上游代码或素材，先核实具体文件的许可和归属，再保留相应说明。研究内容指纹只能证明记录对应关系，不能证明视觉质量或复用权限。
