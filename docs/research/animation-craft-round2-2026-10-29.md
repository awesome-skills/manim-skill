# 持续融合 · 第二轮

用户要求持续推进，直到明确停止。本轮扩大题材与方法来源，并用独立中文缓存任务检查指导的实际行为。整体目标仍进行中。

## 扩展筛查

上一轮 30 个项目之外，本轮成功读取 10 个新仓库的 README 或相关部分；另 4 个候选路径返回 404，单列在 JSON，不计入已读数量。筛查不是运行验收，也未采用星数作为质量指标。

| 项目 | 观察与决定 |
|---|---|
| [Coldtype](https://github.com/coldtype/coldtype) | 程序化字体与按词编排；进一步读两个动画样例。Apache-2.0；借鉴文字与节奏对应，未引入引擎和字体 |
| [Datamations](https://github.com/microsoft/datamations) | 分组保留记录身份，计数分成分组与汇总；深入读 R 实现。DESCRIPTION 为 MIT + LICENSE。用 CE 原创实现数据计数故事 |
| [p5.js](https://github.com/processing/p5.js) | 创意编程与迭代草图；本轮参考入口，未深入运行时 |
| [Two.js](https://github.com/jonobr1/two.js) | 多渲染后端的二维图形接口；暂不需要第二运行时 |
| [d3-transition](https://github.com/d3/d3-transition) | 状态插值和属性 tween；进一步读 attrTween，保留显式状态驱动原则 |
| [Popmotion](https://github.com/Popmotion/popmotion) | 弹簧、关键帧；读 spring 的阻尼分支和停止条件。没有把弹簧套到数据数值上 |
| [Motion Graphics Skill Pack](https://github.com/imMamdouhaboammar/motion-graphics-skills) | README 声明 All Rights Reserved；未复制或融合其技能正文/素材 |
| [code2video](https://github.com/iwerry/code2video) | 叙事意图与技术可用性分开、时间线与检查证据分开；MIT。深入读 storyboard，借鉴轻量记录，不照搬模块/契约平台 |
| [Manim DSA](https://github.com/F4bbi/manim-dsa) | 带样式的数组/栈/图对象；README MIT。保留领域插件入口，未安装或宣称 CE 0.22 兼容验收 |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | 视频构图与网页 token 区分、按手机宽度检查、记录具体修订；README Apache-2.0。深入读 look/review，融合显示尺寸检查，不引入浏览器渲染栈 |

[来源 JSON](animation-craft-round2-2026-10-29.json) 与[补充源码记录](animation-craft-round2-deep-2026-10-29.json)记录文件 SHA 与链接。版权许可只记录实际见到的文件/声明，没有核验到的项目不补猜许可。

## 实际视觉观察

- 打开 Datamations 官方 Examples：看到分组后的点阵和计数结果页；Replay 按钮被 SVG 拦截，因此未声称完整观看其过渡动画。
- 打开 HyperFrames 官方 Inspiration：导航跳转到 examples，最终页面可读；动态横向展廊导致目标播放按钮不可见，截图只作为样式/题材范围的观察，未声称观看完整影片。随后通过页面中实际视频地址打开 “Going through a change”，在 2/5/9/14/19 秒查看真实画面：文字尺度对比、单词与物件结合、场景明暗切换。它仍是浏览器定点观察，未据此声称完整节奏/声音审查。
- 原站图像与媒体未复制到本项目的分发资源。浏览器截图在忽略的 verification 目录，研究记录保留源链接。

## 这轮落地

1. `examples/data_to_decision.py`：24 条合成记录 → 三组 → 6/10/8 个等高单位计数柱。保留原对象和来源身份，最终结论从数据计算。首版小屏类别太小，已增大并缩短辅助文字。
2. `video_inspection.py --preview-width 360`：直接用最终 MP4 生成指定显示宽度的预览，保持画幅比例及原始取证帧。默认行为兼容旧调用。
3. 独立缓存试用发现“命中移走原条目”的错误比喻；反馈后保留缓存 A、返回副本，用 B 解释未命中，并进一步检查运动路径标记遮挡。
4. 对应方法写入 `animation-recipes.md` 与 `aesthetic-refinement.md`，不把单次问题膨胀成新引擎/平台。

## 下一轮仍需做

- 继续扩展实际成片观察和源码深读，尤其是文字编排、空间/相机叙事与几何解释。
- 用新题材继续检验；当前已有样片与一次独立反馈试用，不能证明普遍生成质量提升。
- 检查动作过程、词句阅读时间与跨尺寸表现，避免把静帧构图作为全部动画质量。

具体过程与失败修订见[检查点记录](../evaluations/continuous-craft-20261029/review.md)。

## 后续扩展筛查

继续搜索 camera / physics 后，读取了 [Matheart/manim-physics](https://github.com/Matheart/manim-physics)、[johnhenry/ecmanim](https://github.com/johnhenry/ecmanim)、[hartnady/manim-skill](https://github.com/hartnady/manim-skill) 的 README。前者提示维护时间受限，第二个探索 TS/Node/浏览器多后端，第三个强调 GL/CE 分界。本轮未引入这三个运行时或正文，也没有运行兼容验证。另一个 README 路径404，不计入已读。见[第三批筛查来源](animation-craft-round3-screen-2026-10-29.json)。累计成功筛查43个不同仓库，数量不是质量得分。
