# 父代理反馈后的修订

这不是独立首轮通过。保留上一级目录的首轮源码、视频、检查记录；本目录为反馈后修订。

- 放大了杠杆，重物臂和用力臂各使用支架下方独立的尺寸通道。画面标明「理想杠杆 · 竖直用力 · 缓慢保持平衡」。
- 用单一模型 W=1、重物臂 a=2、用力臂 r 从 2 连续变到 4，F=W*a/r。两支力箭头采用同一长度尺度；施力点、尺寸线和施力箭头由 r 同步更新。终点的半力与两倍力臂由此得到。
- 环境：Python 3.13.16，Manim Community 0.22.0，Cairo，Hiragino Sans GB。参考文件沿用首轮记录。
- 草稿命令：`uv run python -m manim render -ql --media_dir verification/lever-forward-20261030/revision/draft-media verification/lever-forward-20261030/revision/lever.py Lever`
- 最终命令：`uv run python -m manim render -qm --media_dir verification/lever-forward-20261030/revision/final-media verification/lever-forward-20261030/revision/lever.py Lever`
- 草稿抽查 4、8、10、12、14、17、20 秒。最终视频解码为 1280×720、30fps、20.7 秒；抽查 4、7、8、9、10、11、12、13、14、17、20 秒及 360px 的 6、9、11、13、16、20 秒。连续样本显示施力位置向外、箭头缩短，尺寸标注与支架分开；360px 下次要模型条件和力臂标签仍较小，但可以辨认。没有做实时全片播放；检查是采样帧和转场检查。JSON 中 visual_review 为工具默认值，不代表上述人工观察。
- 这是静态平衡的连续示意，非动力学模拟；没有旁白。美观与节奏是主观判断，未获用户确认。
