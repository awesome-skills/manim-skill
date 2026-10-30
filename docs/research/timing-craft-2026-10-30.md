# 时间进度与位置曲线

新增读取三个仓库 README，累计成功筛选 67 个不同仓库。数量不代表动画品质。来源指纹见 [JSON](timing-craft-2026-10-30.json)。

- [Tween.js](https://github.com/tweenjs/tween.js)：README 展示对属性插值、独立 easing 与由调用者驱动的更新时间。借鉴时间和属性分离，不引入 JS 引擎。
- [Shifty](https://github.com/jeremyckahn/shifty)：README 展示 from/to、easing、duration，以及 await 串联动作。仅借鉴动作完成后再推进下一段的组织方式；不采用其性能宣传作为本项目证据。MIT 仅为 README 声明，未做文件级许可核查。
- [D3 Ease](https://github.com/d3/d3-ease)：README 将 easing 解释为时间重映射。进一步读取 [cubic.js](https://github.com/d3/d3-ease/blob/main/src/cubic.js)，其 cubicInOut 是分段三次式；本例没有照搬，采用满足端点速度为零的三次 Hermite 式。实际读取 [LICENSE](https://github.com/d3/d3-ease/blob/main/LICENSE)，为 BSD-3-Clause 文本。

没有运行或观看上述项目的完整演示。原创 `MotionTiming` 同时比较同路径、同四秒时长的匀速与缓入缓出，再以每半秒一个位置标记展示速度差异。共享时钟线性推进，只在位置映射中应用缓动，避免重复缓动。再次演示前显式淡出并复位。没有第三方代码或素材移植，也没有新增依赖。

这不是宣称缓动总比匀速更高级：物理速度、能量或时间有含义时，应保持真实时钟。视觉节奏要支持所解释的内容。样片与检查见[评估](../evaluations/motion-timing-20261030/review.md)。
