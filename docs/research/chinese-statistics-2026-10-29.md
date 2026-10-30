# 中文统计讲解 · 来源筛选与融合

本轮新增读取 4 个仓库 README，累计 47 个成功读取的不同仓库（筛选数量不是质量分数）。来源、内容指纹与已有文件 SHA 见 [JSON](chinese-statistics-2026-10-29.json)。

| 来源 | 本轮实际读取 | 判断 |
| --- | --- | --- |
| [kelvinleandro/manim-animations](https://github.com/kelvinleandro/manim-animations) | README、`src/normalization.py` | 同一组点在固定坐标下移动，适合对照变化；源示例随机数据没有固定种子，本轮采用明确的五条合成记录。未核实许可证，不复制代码。 |
| [rishabhbhartiya/STATANIM](https://github.com/rishabhbhartiya/STATANIM) | README | 统计对象、动画和主题的分层值得继续考察；README 标注 MIT，本轮未安装或验证运行兼容性。 |
| [CountCamp/ManimProject](https://github.com/CountCamp/ManimProject) | README | 内容仅环境命令，不能据此判断动画质量，不作为质量依据。 |
| [Praedyth9/Manim_for_stats](https://github.com/Praedyth9/Manim_for_stats) | README | 含旧 Manimlib / Python 3.7 用法，不作为 CE 0.22 可运行配方。 |

另读 [Manim CE Text 源码](https://github.com/ManimCommunity/manim/blob/main/manim/mobject/text/text_mobject.py)，并用已安装 CE 0.22 实测 `width` 是缩放而非换行：同一句中文在 40 字号下约 12.417×0.550，指定 width=5 后变成 5.000×0.221；显式分两行后为 7.335×1.143。字体为本机 PingFang SC，不推广为其他字体的固定尺寸。

融合结果：原创中文平均值/中位数样片，以固定坐标轴保留离群点的距离含义；同一 tracker 驱动数值、位置、平均值和排序行。根据实际小屏采样，修复数字字体不一致、缺少排序依据和局部标签拥挤。没有引入外部运行依赖或复制上游实现。详见[本轮评估](../evaluations/chinese-statistics-20261029/review.md)。
