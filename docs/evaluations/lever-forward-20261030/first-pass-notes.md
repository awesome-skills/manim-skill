# 杠杆动画试验记录

- 方向：深色简洁的科学示意，固定支点与重物，用两组力臂和力的对照解释平衡；蓝色表示重物、金色表示施力，文字补充含义。
- 分镜：提出问题；等长力臂的平衡；力臂变为两倍；显示一半力的平衡；总结力与力臂的关系。取竖直力、忽略杠杆自重和摩擦的理想示意。
- 实际读取：SKILL.md、references/visual-direction.md、references/aesthetic-refinement.md、references/animation-recipes.md。
- 环境：macOS，Python 3.13.16，Manim Community v0.22.0，Cairo，Hiragino Sans GB（本机字体，其他机器需要该字体或替换）。
- 初稿命令：`uv run python -m manim render -ql --media_dir verification/lever-forward-20261030/draft-media verification/lever-forward-20261030/lever.py Lever`（当时源码保存在 lever-draft.py）。
- 最终命令：`uv run python -m manim render -qm --media_dir verification/lever-forward-20261030/final-media verification/lever-forward-20261030/lever.py Lever`
- 初稿抽查 2、5、8、10、12、14、16、18、20 秒。发现远处仍显示原力且杠杆水平，易误读为平衡；没有明确重物力箭头；用力标签重复。修订为先淡出近处力、延长力臂后再展示半力，加重物向下的力箭头，简化标签。
- 最终抽查 4.7、8、10.5、11.5、12.5、14、15、16、18、20 秒；360px 宽另检查 8、12.5、16、20 秒。画面无明显裁切，中文可辨；手机尺寸的力臂小标签偏小。检查为解码帧及转场采样，未做实时全片播放。report.json 的 visual_review 字段是工具默认值，以上为人工视觉观察。
- 局限：画面是两个理想平衡状态的示意，不是动力学模拟；过渡中水平杆作为静态参照，未实际展示翘起或抬升，动态因果证据有限。审美为作者主观检查，尚未得到用户认可。无旁白或音轨。
