"""Chinese visual-design evaluation; needs a locally installed CJK font."""
import statistics
import manimpango
from manim import (
    Scene, Text, Dot, Line, VGroup, ValueTracker, DecimalNumber,
    FadeIn, FadeOut, Create, always_redraw, LEFT,
)


class MeanMedianStory(Scene):
    def construct(self):
        installed = set(manimpango.list_fonts())
        font = next((f for f in ['Noto Sans CJK SC', 'Source Han Sans SC',
                                 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei']
                     if f in installed), None)
        if not font:
            raise RuntimeError('Install a CJK font or select one with verified Chinese glyph coverage.')
        class Numeral(Text):
            def __init__(self, value, **kwargs):
                super().__init__(value, font=font, **kwargs)

        paper, ink, muted = '#F5F0ED', '#343C53', '#6D7180'
        rose, green = '#B34866', '#367B70'
        self.camera.background_color = paper

        def text(words, size=32, color=ink):
            return Text(words, font=font, font_size=size, color=color)

        def left(obj, x, y):
            return obj.move_to([x, y, 0], aligned_edge=LEFT)

        title = left(text('平均数，为什么会被拉走？', 48), -6.0, 3.05)
        subtitle = left(text('从小到大', 30, muted), -6.0, 2.25)
        source = left(text('示例数据 · 单位：分钟', 26, muted), -6.0, -3.45)
        self.add(title, subtitle, source)
        value = ValueTracker(4)
        x = lambda number: -5.6 + .56 * number
        baseline = Line([x(0), -1.35, 0], [x(20), -1.35, 0], color=muted, stroke_width=1.5)
        ticks = VGroup(*[text(str(n), 28, muted).move_to([x(n), -1.8, 0]) for n in [0,5,10,15,20]])
        fixed = [2,3,3,4]
        heights = [-.25, .42, -.25, .42]
        marks = VGroup(*[
            VGroup(Line([x(v), -1.35, 0], [x(v), y, 0], color=muted, stroke_width=1),
                   Dot([x(v), y, 0], radius=.11, color=ink))
            for v,y in zip(fixed,heights)
        ])
        moving = always_redraw(lambda: VGroup(
            Line([x(value.get_value()),-1.35,0],[x(value.get_value()),-.25,0],color=rose,stroke_width=2),
            Dot([x(value.get_value()),-.25,0],radius=.14,color=rose)))
        moving_number = DecimalNumber(4, num_decimal_places=1, font_size=32, color=rose, mob_class=Numeral)
        moving_number.add_updater(lambda m:m.set_value(value.get_value()).move_to([x(value.get_value()),.08,0]))
        ordered = VGroup(*[text(str(v), 36, green if i == 2 else ink).move_to([-3.2+i*1.25,2.25,0]) for i,v in enumerate(fixed)])
        ordered_last = DecimalNumber(4, num_decimal_places=1, font_size=36, color=rose, mob_class=Numeral)
        ordered_last.add_updater(lambda m:m.set_value(value.get_value()).move_to([1.8,2.25,0]))
        order_note = left(text('第 3 个是中位数', 28, green),3,2.25)
        self.add(ordered, ordered_last, order_note)
        self.next_section('five_people')
        self.play(Create(baseline), FadeIn(ticks), FadeIn(marks), FadeIn(moving), FadeIn(moving_number), run_time=1)
        self.wait(1.6)

        mean_name = left(text('平均值', 32, rose), -1.4, 1.55)
        median_name = left(text('中位数', 32, green), 2.8, 1.55)
        mean_number = DecimalNumber(3.2, num_decimal_places=1, font_size=54, color=rose, mob_class=Numeral)
        median_number = DecimalNumber(3, num_decimal_places=0, font_size=54, color=green, mob_class=Numeral)
        mean_number.add_updater(lambda m:left(m.set_value((sum(fixed)+value.get_value())/5), .35, 1.55))
        median_number.add_updater(lambda m:m.set_value(statistics.median(fixed+[value.get_value()])).move_to([5.1,1.55,0]))
        caption = text('排序后第 3 个是 3；平均值是 3.2', 34).move_to([0,-2.65,0])
        self.next_section('compare_summaries')
        self.play(FadeIn(mean_name),FadeIn(mean_number),FadeIn(median_name),FadeIn(median_number),FadeIn(caption),run_time=.7)
        self.wait(2)
        self.play(FadeOut(caption),run_time=.25)
        caption = text('只改变最后一个人：4 分钟 → 18 分钟', 34).move_to([0,-2.65,0])
        self.play(FadeIn(caption),run_time=.35)
        self.next_section('outlier')
        self.play(value.animate.set_value(18),run_time=3.5)
        self.wait(1.8)
        self.play(FadeOut(caption),run_time=.25)
        caption = text('平均值升到 6；中间那个数仍然是 3', 34).move_to([0,-2.65,0])
        self.play(FadeIn(caption),run_time=.35)
        self.wait(2.8)
        for mob in [moving,moving_number,mean_number,median_number,ordered_last]:mob.clear_updaters()
