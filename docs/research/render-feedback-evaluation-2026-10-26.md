# 渲染反馈与教学评估：用于一次真实新会话试验

2026-10-26。建议采用“冻结任务 + 分层证据 + 带时间的问题记录 + 有界修订”，先做一次未见任务试验；不引入综合美观分。
本次阅读官方源码、数据记录与论文，未安装项目、调用外部模型、运行训练或复现其指标；本报告没有证明当前 skill 的输出效果。

## 快照与许可

用 `gh api repos/OWNER/REPO` 和 `gh api repos/OWNER/REPO/commits/HEAD` 核对；两仓库均未标记 archived。

| 项目 | 默认分支 / 提交 | 提交日期 UTC | 许可证据 |
|---|---|---|---|
| AI4Learning-Club/OmniManim | main / `6a6041fd45300a9220f5d4d6c1c74105a3751697` | 2026-03-21 | API license=null；README 为“按需自定”，树中未见 LICENSE |
| marcelo-earth/generative-manim | main / `f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e` | 2026-09-17 | LICENSE 标 Apache License 2.0 |

许可标识仅转录；OmniManim 的公开可读不等于已取得可复用代码/数据许可。[Omni README][omni-readme]、[Generative LICENSE][gen-license]
本报告只记录机制与来源，不复制候选项目实现。默认分支、发布包、论文实验版本是不同证据。

## OmniManim：诊断记录有用，公开代码中的总分不宜直接做门槛

- `FrameFeatures` / `SegmentFeatures` 保存 frame/sec、片段范围、像素重叠、密度、运动、闪现及 OCR；`EvalReport.issues` 包含 segment、time_range、reason、final_status。[CV][omni-cv]、[fusion][omni-fusion]
- 时间连续性是启发式：相邻帧像素变化量、连通区域变化、运动能量跳变；不是对象身份追踪、物理轨迹证明或主观流畅度。[CV][omni-cv]
- 颜色/亮度掩码及固定密度阈值有适用前提；例如亮背景、数学上有意重叠和静止的阅读段不能仅凭阈值当作失败。此处是检测机制的适用性判断，非实测误报率。
- 公开 VLM prompt 专审可疑重叠，并规定 filled shapes 重叠即 FAIL；输入为片段元数据和关键帧，没有原始题目、教学真值或完整声音。[vlm_judge.py][omni-vlm]
- 因而字段名 `vlm_semantic` 不能直接解释为“教学正确”。fusion 在跳过 VLM 时返回该维度 1.0；UNKNOWN/API_ERROR 也没有按 FAIL 计数。[fusion][omni-fusion]
- evaluator 默认关闭 OCR，而 fusion 对零 OCR artifact 给 rendering=1.0；所以该分数可能表示“未检测”，并非“公式无乱码”。[evaluator][omni-evaluator]、[fusion][omni-fusion]
- pipeline 会依据 overall_score/overall_passed 提早结束或选两轮最高分；直接复制这种门槛会把上述检测范围限制隐藏掉。[主流程][omni-main]
- 兼容性/成本：requirements 仅写 `manim>=0.18.0`，另需 OpenCV、OpenAI SDK，OCR/TTS 有额外条件；这不证明 CE 0.22 集成成功。[requirements][omni-requirements]
- **采用**片段/时间/原因/证据结构与局部修复；**暂缓**CV/VLM接入；**拒绝直接沿用**其总分作为审美、教学或运动验收门槛。

## 论文中的学习组件必须单列

[OmniManim 论文 v1][omni-paper] 描述训练的布局先验/坐标去噪与插值约束，并报告消融；这不同于上述仓库快照中的提示词与 CV 流水线。
所查仓库树没有找到该布局训练器/权重；论文 C.3 仍列研究代码/数据的发布计划，不能据公开 demo 声称已复现论文。
论文 D/E/F 分别讨论任务判断、视觉指标和整片人工观看，且明确 CV 不能替代教学、事实及审美判断；应保留这些区分。
本次没有验证学习组件收益能否迁移到当前 skill，也没有证据断言它们“没有必要”；暂缓是当前试验规模与可用实现所决定。

## Generative Manim：可执行 benchmark 与学习目标到底测什么

- `core_v1.jsonl` 冻结 task_id/category/difficulty/prompt、required/disallowed regex 与最少动画数；便于复用任务和归类失败。[任务][gen-tasks]、[checks][gen-checks]
- `verify_code` 以 Manim 子进程 exit=0 判 success，动画数从 stderr 解析；没有读取渲染图像或证明视频完整解码。[verifier][gen-verifier]
- `benchmarks/run.py` 的 score=0.7×render_success+0.2×required_regex覆盖+0.1×动画数比例；disallowed 匹配另列记录。
  更关键的是 task_pass/pass@k 只统计 `verify_result.success`，并没有把 regex 与教学正确性合成通过定义。[run.py][gen-run]
- `Axes(`、`MathTex(` 或 `self.play()` 出现在代码中，不证明它实际解释了要求；正确 CE 替代 API 也可能被 regex 漏掉。此为静态检查性质判断。[checks][gen-checks]
- 训练确有实现：SFT 使用 QLoRA/TRL；DPO 配对选可渲染且动画数最多的输出与失败输出；GRPO reward 为渲染成功加 `self.play` 次数封顶奖励。[SFT][gen-sft]、[DPO][gen-dpo]、[reward][gen-reward]
- `GRPOTrainer` 接入上述 reward 更新模型；因此这是训练代码，不是仅给通用模型加提示词。但奖励没有教学真值/画面诊断，不能据此声称学到了美观或正确教学。[GRPO][gen-grpo]
- 兼容性/成本：training requirements 固定 `manim==0.21.0`，并引入 torch/transformers/trl/peft/bitsandbytes；verifier CLI 含 `--custom_folders`。不能直接拿来当本项目 CE 0.22 的已验证基准。[requirements][gen-requirements]、[verifier][gen-verifier]
- **采用**冻结任务、逐样本记录、首次与修订分开；**暂缓**训练栈与完整 benchmark 接入；**拒绝把**渲染 pass@k、regex 或动画次数叫作教学/审美成功率。
- 不增加 VisualEDU：以上已足以确定本次记录与试验边界；不需要为一个小规模试验继续扩候选清单。

## 最小试验：先冻结判据，再让新会话独立完成

父任务已启动独立试用：15–25 秒中文最大堆取顶后下沉，树与数组对应；本调研未读取或影响其产出。
复用父任务事先冻结的算法、对应、交付、解释、布局判据，记录必须看见的因果动作、状态不变量和困难过渡；不另造第二套接受标准。
只交付任务、skill 路径和正常环境信息；保存首次结果。若允许一次反馈修订，保持同一任务与判据，完整保留初版/终版及反馈，分别报告。
一个任务只能证明一个案例的可行性；修复后的成功不等于首次成功，也不能据一次试验估计普遍 pass@k 或培训效果。

| 必记部分 | 最少证据与判定 |
|---|---|
| 身份/条件 | task_id、冻结 prompt/判据、skill SHA、模型/推理设置、Python/Manim、依赖、seed、尺寸/FPS；未能读取的值标 unknown |
| 可执行性 | 命令、exit、日志、媒体路径/hash、完整解码结果、实际时长/尺寸；环境失败与场景失败分开 |
| 视觉诊断 | 实际时间戳的静帧/过渡采样；按具体遮挡、裁切、字号、焦点问题记 pass/fail/not_checked，不写“总体8分” |
| 教学正确 | 每个必需结论/不变量的真值与画面动作逐项对应；公式/算法源码核对和观看证据分别记录；错误不能被美观抵消 |
| 时间连续性 | 原速观看范围、困难区间循环/逐帧范围；身份保持、误导性中间状态、短暂闪现、阅读停留；只看截图则 not_checked |
| 表达判断 | 审查者和观察条件，具体指出哪里让关系更易/难理解；属于观察判断，不假装客观美学量表 |
| 修订成本 | 每次错误/反馈、改动、重复渲染次数与耗时；首版、修订版各自的源码/媒体/hash，不只保留最好结果 |
| 学习效果 | 若没有真实目标受众的理解/迁移回答，标 not_measured；审查者认为清楚不能替代学习提升证据 |

每个问题一条最小记录：`需求/判据 | 片段时间 | 可见症状 | 局部修改 | 复查证据 | 状态`，证据链接指向确切版本的媒体。
致命的教学错误、漏掉必需动作或读不清关键对象即该项失败；未检查保持未检查，不让其他项的通过抵消。
这是一份有来源的人工/代理观察记录，不是新建评分框架；先用一次真实产出验证它是否能指导具体修复，再决定是否值得自动化。

## 本轮实测记录

独立代理的最终产出与父代理复核见[最大堆下沉试用](../evaluations/heap-repair-20261026/review.md)。它验证一次限定任务的可行性；原速播放、首次成功率、学习效果和旧版对照保持未验证/未测量，不并入任何总分。

## 固定来源

[omni-readme]: https://github.com/AI4Learning-Club/OmniManim/blob/6a6041fd45300a9220f5d4d6c1c74105a3751697/README.md
[omni-cv]: https://github.com/AI4Learning-Club/OmniManim/blob/6a6041fd45300a9220f5d4d6c1c74105a3751697/eval_pipeline/cv_features.py
[omni-fusion]: https://github.com/AI4Learning-Club/OmniManim/blob/6a6041fd45300a9220f5d4d6c1c74105a3751697/eval_pipeline/fusion.py
[omni-vlm]: https://github.com/AI4Learning-Club/OmniManim/blob/6a6041fd45300a9220f5d4d6c1c74105a3751697/eval_pipeline/vlm_judge.py
[omni-evaluator]: https://github.com/AI4Learning-Club/OmniManim/blob/6a6041fd45300a9220f5d4d6c1c74105a3751697/agent_pipeline/evaluator.py
[omni-main]: https://github.com/AI4Learning-Club/OmniManim/blob/6a6041fd45300a9220f5d4d6c1c74105a3751697/agent_pipeline/main.py
[omni-requirements]: https://github.com/AI4Learning-Club/OmniManim/blob/6a6041fd45300a9220f5d4d6c1c74105a3751697/requirements.txt
[omni-paper]: https://arxiv.org/html/2605.15585v1
[gen-license]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/LICENSE
[gen-tasks]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/benchmarks/tasks/core_v1.jsonl
[gen-checks]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/benchmarks/checks.py
[gen-run]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/benchmarks/run.py
[gen-verifier]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/rendering/manim_verifier.py
[gen-sft]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/stages/sft_train.py
[gen-dpo]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/data/generate_dpo_pairs.py
[gen-reward]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/rendering/reward.py
[gen-grpo]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/stages/grpo_train.py
[gen-requirements]: https://github.com/marcelo-earth/generative-manim/blob/f681cc78a6b1cad8443b6af4b3a1adbfed9d3e0e/training/requirements.txt
