# 动画创作项目调研与融合

2026-10-29。目标：让当前 Manim Skill 更善于生成构图清楚、动作连贯、风格合适的解释动画，并把方法落实为可运行的 CE 示例与检查入口。

## 范围与证据

本轮以 GitHub 仓库搜索为入口，检索数学动画、程序化视频、动态图形、时间线编辑器、Manim skill 和程序化动画等方向，筛选并阅读 **30 个仓库的 README**，对其中 **10 个仓库的 12 份源码/文档**进一步检查。元数据、README blob SHA 和深入阅读的文件 SHA 见[来源清单](animation-craft-2026-10-29.json)。README 首轮取样后，对采用的机制继续读对应文件；这是定向调研，不是全仓审计。

GitHub 搜索曾触发临时限流；暂停搜索、阅读公开文档后继续。未把未读取的命中项计入 30 个项目。未运行上游引擎，未测它们的性能、兼容性或生成质量；README 的宣传性描述不构成效果证明。许可证列是 GitHub 元数据与 README 的筛查结果，不是对所有子目录/素材的法律审计。没有复制上游实现、字体或媒体。

## 候选矩阵

“采用”指借鉴方法并用 CE 原创实现；“参考”指仅保留按需入口；“暂缓”指本轮不接入运行时。

| 项目 | 观察到的机制 / 适用方向 | 许可筛查 | 本轮决定 |
|---|---|---|---|
| [3b1b/manim](https://github.com/3b1b/manim) | 程序化数学动画，独立 ManimGL 引擎 | MIT | 参考几何解释；保留 CE |
| [3b1b/videos](https://github.com/3b1b/videos) | 交互 checkpoint 与局部重做工作流 | CC BY-NC-SA 4.0（README） | 采用短片段迭代；不复制视频源码/素材 |
| [ManimCommunity/manim](https://github.com/ManimCommunity/manim) | 当前可执行基底与公开场景 API | MIT | 保持锁定的 0.22.0 环境 |
| [jkjkil4/JAnim](https://github.com/jkjkil4/JAnim) | 实时预览、子时间轴分离动画逻辑 | MIT | 借鉴可独立调整的段落；暂缓引擎 |
| [AzurIce/ranim](https://github.com/AzurIce/ranim) | Rust 动画引擎；README 明示 API 仍不稳定 | MIT | 参考，暂缓 Rust 运行时 |
| [academa-labs/manimgx](https://github.com/academa-labs/manimgx) | 数学场景、GPU 引擎；线性映射示例区分旋转与逐项插值 | MIT | 采用“中间状态也要满足解释”的检查原则；不声称加速/兼容 |
| [maloyan/manim-web](https://github.com/maloyan/manim-web) | 浏览器播放器、时间拖动、片段导航 | MIT | 借鉴成片导航；暂缓 TS 引擎移植 |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | 相对布局、重叠启动的 sequence、编辑预览 | MIT | 采用布局锚点及错峰语义，映射到 CE |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | 参数化视频、设计系统、Player/Studio | 自定义许可证 | 借鉴命名视觉参数与预览/交付一致性；不引入其实现 |
| [midrender/revideo](https://github.com/midrender/revideo) | 自包含场景组件、相同项目驱动预览与渲染 | MIT | 采用同一成片检查；暂缓浏览器渲染栈 |
| [theatre-js/theatre](https://github.com/theatre-js/theatre) | 可视化与程序化编辑变量/时间线 | Apache-2.0 | 参考可编辑动作参数；不新建编辑器 |
| [juliangarnier/anime](https://github.com/juliangarnier/anime) | 缓动、中心/起点等 stagger 顺序 | MIT | 采用按语义选择揭示顺序与动作速度 |
| [motiondivision/motion](https://github.com/motiondivision/motion) | 共享 layout ID 与中点位置测试 | MIT（核心） | 采用稳定对象身份与过渡中点检查；不借用付费素材 |
| [mojs/mojs](https://github.com/mojs/mojs) | shape、burst、stagger 等可组合动作 | MIT | 参考局部强调；不默认堆叠粒子效果 |
| [airbnb/lottie-web](https://github.com/airbnb/lottie-web) | 设计工具导出动画数据，运行时播放 | MIT（运行时） | 参考，当前无需 AE/Lottie 资产管线 |
| [rive-app/rive-runtime](https://github.com/rive-app/rive-runtime) | artboard、状态机、运行时绘制 | MIT（运行时） | 借鉴状态转移思路；不把编辑器/资产一并视作 MIT |
| [GraphiteEditor/Graphite](https://github.com/GraphiteEditor/Graphite) | 非破坏式图形与节点化编辑；README 含未来路线 | Apache-2.0 | 参考；不把规划能力当已验收功能 |
| [alyssaxuu/motionity](https://github.com/alyssaxuu/motionity) | 关键帧、缓动、遮罩、文本动画 | MIT | 参考图层与时序；暂缓编辑器集成 |
| [excalimate/excalimate](https://github.com/excalimate/excalimate) | 图解顺序揭示、时间线、相机与 MCP | MIT | 采用有序揭示；不要求 Excalidraw/MCP |
| [philip-murray/reactive-manim](https://github.com/philip-murray/reactive-manim) | 项身份、clone/merge、固定锚点的公式组合 | MIT | 保留显式身份原则；README 版本约束需单独兼容验证 |
| [helblazer811/ManimML](https://github.com/helblazer811/ManimML) | 网络层组合与 forward-pass 动画 | MIT | 借鉴先建结构再展示传播；领域插件按任务评估 |
| [ManimCommunity/manim-voiceover](https://github.com/ManimCommunity/manim-voiceover) | 旁白时长与词级触发 | MIT | 有旁白需求时再接入，不生成虚构同步证据 |
| [jeertmans/manim-slides](https://github.com/jeertmans/manim-slides) | 片段暂停、循环、现场控制 | MIT | 现场演示按需入口，普通视频保留 sections |
| [HarleyCoops/Math-To-Manim](https://github.com/HarleyCoops/Math-To-Manim) | 生成项目、源码/视频/拼图与制作记录 | MIT | 借鉴可核对交付记录；不采信未渲染作品的质量 |
| [marcelo-earth/generative-manim](https://github.com/marcelo-earth/generative-manim) | LLM→Manim 生成管线与应用 | Apache-2.0 | 参考；当前 Agent 已负责生成，无需重复平台 |
| [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) | CE/GL 分离的参考组织 | MIT | 参考引擎分界；不照抄旧安装版本信息 |
| [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) | 分领域创作包、冻结时刻、拼图、成片规格检查 | MIT | 采用轻量反馈入口；保留现有 PyAV 解码实现 |
| [iart-ai/manim-skills](https://github.com/iart-ai/manim-skills) | 场景/对象/动画指导与单帧验证入口 | MIT | 参考路由；本项目继续要求视频与过渡检查 |
| [Elteoremadebeethoven/AnimationsWithManim](https://github.com/Elteoremadebeethoven/AnimationsWithManim) | 文字、变换、图形教学，基于 2019 版引擎 | 未检测到 | 仅参考，暂缓代码复用 |
| [jkjkil4/videos](https://github.com/jkjkil4/videos) | JAnim 视频源码集合 | 未检测到 | 仅筛查，未深入源码，不复制 |

## 融合落点

### 1. 对象身份成为画面中的连续线索

Motion 的共享元素样例明确测试同一 layout ID 在过渡中点的位置；reactive-manim 的公式样例通过 clone、merge 与锚点区分重复项。共同启发是：先决定“哪个东西仍是同一个东西”，再决定它的外观怎么变。

落地：[MergeStep](../../examples/merge_step.py) 用 `(来源, 原索引)` 标识卡片，真实归并事件决定选择顺序，原卡片沿运动通道进入结果。重复值稳定性由语义测试覆盖。它是原创的短解释，不是对已有快排示例的整体替换。

### 2. 让节奏和中间状态服务于含义

Motion Canvas 的 `sequence` 以固定间隔启动任务，并允许重叠；Anime.js 的 stagger 支持不同起点。融合时明确 CE 的 `lag_ratio` 是相对偏移，外层 `run_time` 会缩放整个组，避免把 JS 的毫秒延迟直接搬来。

ManimGX 线性映射源码区分真实旋转与矩阵逐项插值，提醒我们终点正确不能证明过程正确。落地：[WaveSuperposition](../../examples/wave_superposition.py) 用一个相位驱动输入与结果，同一 x 的探针同时采样，坐标比例固定。相位只是演示参数，不把缓动速度解释为物理时间。

### 3. 用因果顺序和画幅重排代替统一模板

ManimML 把网络结构与传播动作分开；Excalimate 将揭示顺序显式写入序列。落地：[PacketJourney](../../examples/packet_journey.py) 先显示路线，令牌到达后才强调目的节点，横屏横排、竖屏竖排。三支新示例采用不同的构图，而不是统一加一层仪表盘外框。

### 4. 把实际视频变成可定位的反馈对象

JAnim、Theatre、manim-web 提供了可定位预览的参考；iart-ai 的检查工具强调冻结时刻和成片规格。现有检查器已经能按真实时间戳解码，因此本轮只扩展两个真实缺口：

- `--around/--radius/--samples`：一次检查过渡前后的一组帧；越界时报错。
- `review.html`：离线原生播放器、时间点按钮与速度选择；引用同一 MP4，不重新运行场景，不上传视频。

HTML 播放器不会自动改变 `visual_review`；浏览器跳转不是精确帧取证，PNG/JSON 才记录解码帧。文件路径与名称做 URL 编码和 HTML 转义，测试覆盖带特殊字符的路径。一次测试暴露 macOS `/var` 软链接路径问题，已改为先解析真实路径再计算相对路径。

## 为什么不直接接更多引擎

这轮实际要修的是创作选择和检查入口。新增 Rust、TypeScript、浏览器渲染器或平台服务会同时增加环境、API 和验证范围，且没有现有失败案例证明它们是必要条件。保留来源和按需入口，若之后确有交互编辑、旁白或渲染速度需求，再用具体任务比较。未新增运行时依赖，`uv.lock` 不变。

## 验证入口

- 创作指导：[animation-recipes.md](../../references/animation-recipes.md)，由 SKILL 与 visual-direction 路由。
- 语义与工具测试：`uv run python -m unittest discover -s tests -v`。
- 全部示例：`uv run python scripts/smoke.py --include-typst`；TeX 需外部环境。
- 本轮画面、过渡、规格及未验证项：[验收记录](../evaluations/animation-craft-20261029/review.md)。

这些手写示例验证具体机制可运行；它们不等于独立 Agent 的泛化试验，也不证明相比旧版普遍提高审美、理解率或首次成功率。
