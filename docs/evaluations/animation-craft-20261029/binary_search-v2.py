from manim import *

# Binary search on a sorted row; steps are computed rather than hard-coded.
VALUES = list(range(1, 16))
TARGET = 13
FONT = 'Hiragino Sans GB'
BG = '#101a2b'
MUTED = '#526173'
TEAL = '#61ddca'
GOLD = '#ffcf70'
WHITE_TEXT = '#edf3f8'

def steps(values, target):
    lo, hi = 0, len(values)-1
    while lo <= hi:
        mid = (lo + hi) // 2
        yield lo, hi, mid
        if values[mid] == target:
            break
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

class BinarySearch(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text('二分搜索', font=FONT, font_size=43, color=WHITE_TEXT).to_edge(UP, buff=.42)
        subtitle = Text('在排好序的数字中，找到 13', font=FONT, font_size=28, color=TEAL).next_to(title, DOWN, buff=.18)
        boxes, nums = VGroup(), VGroup()
        for i, value in enumerate(VALUES):
            box = RoundedRectangle(width=.73, height=.78, corner_radius=.10, stroke_width=2, color='#6f8295', fill_color='#233449', fill_opacity=1)
            number = Text(str(value), font=FONT, font_size=27, color=WHITE_TEXT).move_to(box)
            boxes.add(box); nums.add(number)
        boxes.arrange(RIGHT, buff=.095).move_to(UP*.12)
        for box, number in zip(boxes, nums): number.move_to(box)
        ordered = Text('从小到大排列', font=FONT, font_size=24, color='#acbccc').next_to(boxes, UP, buff=.85)
        caption = Text('先看正中间', font=FONT, font_size=32, color=WHITE_TEXT).move_to(DOWN*1.65)
        hint = Text('目标 13', font=FONT, font_size=25, color=GOLD).to_edge(LEFT, buff=.75).shift(DOWN*2.75)
        def candidate_range(lo, hi):
            left = boxes[lo].get_left()[0]
            right = boxes[hi].get_right()[0]
            y = boxes[lo].get_bottom()[1] - .22
            line = Line([left, y, 0], [right, y, 0], color=TEAL, stroke_width=3)
            ends = VGroup(Line([left,y,0], [left,y+.12,0], color=TEAL), Line([right,y,0], [right,y+.12,0], color=TEAL))
            return VGroup(line, ends)

        count = Text('候选：15 个', font=FONT, font_size=25, color=TEAL).to_edge(RIGHT, buff=.75).shift(DOWN*2.75)
        interval = candidate_range(0, 14)
        self.next_section('question')
        self.play(FadeIn(title, shift=UP*.1), FadeIn(subtitle), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(VGroup(b,n), shift=UP*.12) for b,n in zip(boxes, nums)], lag_ratio=.04), FadeIn(ordered), run_time=1.4)
        self.play(FadeIn(caption), FadeIn(hint), FadeIn(count), Create(interval), run_time=.5)
        self.wait(1.5)
        marker = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1).scale(.11).rotate(PI).next_to(boxes[7], UP, buff=.11)
        midlabel = Text('中间', font=FONT, font_size=21, color=GOLD).next_to(marker, UP, buff=.06)
        self.next_section('compare')
        self.play(FadeIn(marker), FadeIn(midlabel), boxes[7].animate.set_stroke(GOLD, width=4), run_time=.7)
        self.wait(.5)
        compare = Text('8 小于 13', font=FONT, font_size=32, color=WHITE_TEXT).move_to(caption)
        self.play(Succession(FadeOut(caption), FadeIn(compare)), run_time=.4)
        self.wait(1.4)
        reason = Text('左边都不可能是 13', font=FONT, font_size=32, color=WHITE_TEXT).move_to(compare)
        self.play(Succession(FadeOut(compare), FadeIn(reason)), run_time=.4)
        proof = Text('1–8 都 ≤ 8 < 13', font=FONT, font_size=23, color=GOLD).move_to([boxes[3].get_center()[0], -.75, 0])
        next_count = Text('候选：7 个', font=FONT, font_size=25, color=TEAL).move_to(count)
        self.play(FadeIn(proof), *[AnimationGroup(boxes[i].animate.set_fill('#172332').set_stroke(MUTED, width=1), nums[i].animate.set_color(MUTED)) for i in range(8)], Transform(interval, candidate_range(8,14)), Succession(FadeOut(count), FadeIn(next_count)), run_time=1.0)
        count = next_count
        self.wait(1.2)
        self.play(FadeOut(proof), run_time=.3)
        # Each following state is computed by the same search routine.
        events = list(steps(VALUES, TARGET))
        previous_mid = events[0][2]
        for lo, hi, mid in events[1:]:
            val = VALUES[mid]
            label = (f'{val} 小于 13，排除左边' if val < TARGET else f'{val} 大于 13，排除右边' if val > TARGET else '找到 13！')
            next_caption = Text(label, font=FONT, font_size=32, color=TEAL if val == TARGET else WHITE_TEXT).move_to(reason)
            self.play(FadeOut(reason), run_time=.2)
            self.play(marker.animate.next_to(boxes[mid], UP, buff=.11), midlabel.animate.next_to(boxes[mid], UP, buff=.4), boxes[mid].animate.set_stroke(GOLD, width=4), FadeIn(next_caption), run_time=.7)
            reason = next_caption
            self.wait(.9)
            if val != TARGET:
                eliminated = range(lo, mid+1) if val < TARGET else range(mid, hi+1)
                new_lo, new_hi = (mid+1, hi) if val < TARGET else (lo, mid-1)
                new_count = Text(f'候选：{new_hi-new_lo+1} 个', font=FONT, font_size=25, color=TEAL).move_to(count)
                self.play(*[AnimationGroup(boxes[i].animate.set_fill('#172332').set_stroke(MUTED, width=1), nums[i].animate.set_color(MUTED)) for i in eliminated], Transform(interval, candidate_range(new_lo,new_hi)), Succession(FadeOut(count), FadeIn(new_count)), run_time=.65)
                count = new_count
                self.wait(.45)
            else:
                self.play(boxes[mid].animate.set_fill('#1b615d').set_stroke(TEAL, width=4), nums[mid].animate.set_color(WHITE_TEXT), run_time=.6)
            previous_mid = mid
        self.next_section('insight')
        final = Text('有序 + 比中间 → 每次排除约一半', font=FONT, font_size=31, color=WHITE_TEXT).move_to(reason)
        self.play(Succession(FadeOut(reason), FadeIn(final)), run_time=.6)
        self.wait(3.0)
