from manim import *
import numpy as np

BG='#101820'; INK='#E8ECE9'; MUTED='#9BAAB0'; GOLD='#D3B77C'; BLUE='#86B8C1'; FONT='Hiragino Sans GB'
config.background_color=BG

def txt(s,size=30,color=INK): return Text(s,font=FONT,font_size=size,color=color)
def line(a,b,color=MUTED,width=1): return Line(a,b,color=color,stroke_width=width)
def iris(radius,center,accent=GOLD):
    c=np.array(center); ring=Circle(radius=1.44,stroke_color='#55646B',stroke_width=2).move_to(c)
    outer=Circle(radius=1.33,stroke_color=INK,stroke_width=1.5).move_to(c)
    # Aperture represented by a dark circular opening, surrounded by a matte annulus.
    disk=Annulus(inner_radius=radius,outer_radius=1.30,color='#384951',fill_opacity=1,stroke_width=0).move_to(c)
    opening=Circle(radius=radius,color=accent,stroke_width=3,fill_color='#080E12',fill_opacity=1).move_to(c)
    ticks=VGroup(*[line(c+1.34*np.array([np.cos(t),np.sin(t),0]),c+1.42*np.array([np.cos(t),np.sin(t),0]),'#7B8A8F',1) for t in np.linspace(0,TAU,32,endpoint=False)])
    return VGroup(disk,opening,ring,outer,ticks)

class Aperture(Scene):
 def construct(self):
    self.next_section('opening')
    header=txt('摄影基础  /  EXPOSURE',20,MUTED).to_edge(UL,buff=.48)
    rule=line(LEFT*6.6+UP*3.15,RIGHT*6.6+UP*3.15,'#4A5B62')
    title=txt('光圈，如何控制进光量？',46).move_to(UP*2.35)
    sub=txt('同一镜头 · 同一快门时间 · 同一场景',25,MUTED).move_to(UP*1.7)
    lens=iris(.80,[0,-.38,0]); caption=txt('光圈是镜头内控制进光的开口',30).move_to(DOWN*2.55)
    self.play(FadeIn(header),Create(rule),FadeIn(title,shift=UP*.1),run_time=1.3)
    self.play(FadeIn(lens),FadeIn(sub),run_time=1.1)
    self.play(FadeIn(caption),run_time=.5); self.wait(2.4)
    self.next_section('opening_changes')
    small=iris(.56,[0,-.38,0]); cap2=txt('开口越大，同样时间进入的光越多',30).move_to(DOWN*2.55)
    self.play(Transform(lens,small),FadeOut(caption),run_time=1.4)
    self.play(FadeIn(cap2),run_time=.5); self.wait(1)
    large=iris(.80,[0,-.38,0]); self.play(Transform(lens,large),run_time=1.4); self.wait(1.4)
    self.next_section('comparison')
    self.play(FadeOut(title),FadeOut(sub),FadeOut(cap2),FadeOut(lens),run_time=.6)
    head=txt('同一焦距下，比较两个光圈',37).move_to(UP*2.5)
    left=iris(.80,[-3.15,.15,0],GOLD); right=iris(.56,[3.15,.15,0],BLUE)
    la=txt('f/2.8',40,GOLD).move_to(LEFT*3.15+DOWN*1.65); lb=txt('f/4',40,BLUE).move_to(RIGHT*3.15+DOWN*1.65)
    note=txt('数字越小，开口越大',30).move_to(DOWN*2.65)
    self.play(FadeIn(head),FadeIn(left),FadeIn(right),run_time=1.1)
    self.play(FadeIn(la),FadeIn(lb),run_time=.5); self.wait(2)
    self.play(FadeIn(note),run_time=.5); self.wait(2.5)
    self.next_section('area')
    self.play(FadeOut(note),run_time=.3)
    # Bars share a scale; 2:1 is the conventional rounded exposure ratio.
    bars=VGroup(Rectangle(width=2.0,height=.12,stroke_width=0,fill_color=GOLD,fill_opacity=1).move_to(LEFT*3.15+DOWN*2.20), Rectangle(width=1.0,height=.12,stroke_width=0,fill_color=BLUE,fill_opacity=1).move_to(RIGHT*3.15+DOWN*2.20))
    result=txt('相对进光量：约 2 倍',31).move_to(DOWN*2.7)
    detail=txt('开口面积 ∝ 1 / f 值²',23,MUTED).move_to(DOWN*3.17)
    self.play(FadeIn(bars),FadeIn(result),run_time=.7); self.play(FadeIn(detail),run_time=.5); self.wait(3.5)
    self.next_section('takeaway')
    self.play(FadeOut(head),FadeOut(detail),FadeOut(result),FadeOut(bars),run_time=.6)
    final=txt('f/2.8 更亮  ·  f/4 进光更少',36).move_to(UP*2.55)
    foot=txt('其他条件相同  /  约相差一挡',26,MUTED).move_to(DOWN*2.6)
    self.play(FadeIn(final),FadeIn(foot),run_time=.7); self.wait(3)
