# 物理动画：模型、约束与表现分开

本轮读取 3 个新项目 README，累计成功筛选 70 个不同仓库。最初使用错误的 `pymunk/pymunk` 地址得到 404，经 GitHub 仓库搜索确认实际为 `viblo/pymunk`；失败地址不计入数量。来源指纹见 [JSON](mechanics-craft-2026-10-30.json)。

| 来源 | 实际读取内容 | 对解释性动画的取舍 |
| --- | --- | --- |
| [Pymunk](https://github.com/viblo/pymunk) | README.rst 中 Space、Body、Shape、固定步长 step 与 debug_draw 分离；README 声明 MIT | 物理状态与画面应由一致的数据连接；不为简单解析关系安装新引擎 |
| [pybox2d](https://github.com/pybox2d/pybox2d) | README 中刚体形状、关节和渲染后端；深入 cantilever.py | 连接关系是模型的一部分，不能只靠图形摆放看起来连接 |
| [use-cannon](https://github.com/pmndrs/use-cannon) | README 说明 cannon-es worker API、React hooks、示例包的分层 | 引擎与表现层可分离；当前 Manim 示例不需要 React/Web Worker 依赖 |

[Cantilever 源文件](https://github.com/pybox2d/pybox2d/blob/master/library/Box2D/examples/cantilever.py)明确创建相邻刚体之间的 weld joint，分别展示固定连接和带阻尼设置的连接。源码头部包含 zlib 风格许可条款；这是单个文件的读取，不代表已完成整个仓库及其依赖的许可核查。未复制其代码。

这次研究没有运行上述物理引擎或观看完整演示，也不借其 README 宣传证明效果。对短小的平衡讲解，解析模型通常足以保持关系；如果展示失衡后的运动，则需要一致的动力学或明确标注示意。不能把任意倾斜插值当作真实受力仿真。

并行进行的新题材 Skill 试作是中文杠杆讲解。独立首轮存在主体偏小、尺寸标注拥挤、相等力使用不同箭头长度的问题；父代理反馈后再修订，不将后续改进归为首轮独立成功。具体结果见[首轮与反馈后修订](../evaluations/lever-forward-20261030/review.md)。
