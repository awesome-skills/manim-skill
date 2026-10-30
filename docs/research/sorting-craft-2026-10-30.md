# 排序动画：事件语义与可读性

本轮成功读取 3 个新仓库的 README，累计筛选 64 个不同仓库。深入读取其中一个算法文件，没有运行上游项目或观看其完整演示；不能据此评价其实际动画观感。来源指纹见 [JSON](sorting-craft-2026-10-30.json)。

| 项目 | 实际读取到的机制 | 对本项目的取舍 |
| --- | --- | --- |
| [SortingAlgorithmAnimations](https://github.com/vbohush/SortingAlgorithmAnimations) | README 列出九种算法及随机、少量不同值、逆序、接近有序四类输入；README 声明 MIT | 保留不同输入的语义检查，不把一个随机样例当通用验证 |
| [sorting-visualizer](https://github.com/zamhown/sorting-visualizer) | Matplotlib 动画，可播放、导出 HTML 或 MP4；同样提供四种输入 | 不引入另一渲染引擎；借鉴输入条件应明确的做法 |
| [sort-visualizer](https://github.com/ramiz-rahman/sort-visualizer) | README 描述算法 trace、颜色语义映射、描述信息分离；README 声明 MIT | 与现有 Event 模型对应，保留事件层，改进视觉表现 |

深入阅读 [QuickSort.js](https://github.com/ramiz-rahman/sort-visualizer/blob/master/src/algorithms/QuickSort.js)，blob `b0e3e249af252220f5324d285088c20abbf8e16c`。实现使用随机枢轴，把比较、交换、较小区域、已排序区域写入 trace。此源文件不证明 UI 如何插值。本项目保留已有确定性的末尾枢轴 Lomuto 事件算法，未复制上游实现。

本地对照发现两点直接影响画面解释：柱子在原位置改变高度会把交换表现成数值变化；无关句子逐字 Transform 会在过渡中出现难读的字形。改进是移动原柱与数字、交换完成后更新位置索引，并对离散决策文字直接切换。同时移除背景大圆和拥挤的侧边 HUD，把图例和计数排列在上方。

本轮没有加入第三方依赖或素材。许可列仅区分 README 声明，不代表完成全部文件级核查。验证与局限见[本地评估](../evaluations/quicksort-craft-20261030/review.md)。
