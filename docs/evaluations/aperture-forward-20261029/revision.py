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
    self.next_section('light_path')
    self.play(FadeOut(title),FadeOut(sub),FadeOut(caption),FadeOut(lens),run_time=.5)
    pathhead=txt('开口大小，决定哪些光线能通过',36).move_to(UP*2.5)
    pathnote=txt('示意：相同入射光与曝光时间',24,MUTED).move_to(UP*1.95)
    # Parallel rays are schematic paths, not literal photon counts or a lens simulation.
    def path(gap):
        wall=VGroup(Line([0,-1.25,0],[0,-gap,0],color=INK,stroke_width=10),Line([0,gap,0],[0,1.25,0],color=INK,stroke_width=10))
        incoming=VGroup(*[Line([-4.3,y,0],[-.12,y,0],color=GOLD,stroke_width=3) for y in [-.8,-.4,0,.4,.8]])
        outgoing=VGroup(*[Line([.12,y,0],[4.3 if abs(y)<gap else .18,y,0],color=GOLD,stroke_width=3) for y in [-.8,-.4,0,.4,.8]])
        blocked=VGroup(*[Dot([-.13,y,0],radius=.055,color=GOLD) for y in [-.8,-.4,0,.4,.8] if abs(y)>gap])
        return VGroup(wall,incoming,outgoing,blocked)
    guide=VGroup(txt('入射光',24,MUTED).move_to(LEFT*3.55+DOWN*1.65),txt('光圈开口',24,MUTED).move_to(DOWN*1.65),txt('通过的光',24,MUTED).move_to(RIGHT*3.55+DOWN*1.65))
    diagram=path(.62); state=txt('较大开口',30,GOLD).move_to(DOWN*2.5)
    self.play(FadeIn(pathhead),FadeIn(pathnote),FadeIn(diagram),FadeIn(guide),run_time=.8)
    self.play(FadeIn(state),run_time=.4); self.wait(1.5)
    smaller=path(.22); nextstate=txt('较小开口，更多光线被挡住',30,BLUE).move_to(DOWN*2.5)
    self.play(FadeOut(diagram[2]),FadeOut(diagram[3]),FadeOut(state),run_time=.3)
    self.play(Transform(diagram[0],smaller[0]),run_time=.7)
    self.play(FadeIn(smaller[2]),FadeIn(smaller[3]),FadeIn(nextstate),run_time=.4); self.wait(1.5)
    self.play(FadeOut(pathhead),FadeOut(pathnote),FadeOut(diagram),FadeOut(smaller[2]),FadeOut(smaller[3]),FadeOut(guide),FadeOut(nextstate),run_time=.5)
    self.next_section('comparison')
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
    barlabels=VGroup(txt('约 2 倍',29,GOLD).move_to(LEFT*3.15+DOWN*2.55),txt('1 倍（基准）',29,BLUE).move_to(RIGHT*3.15+DOWN*2.55))
    result=txt('相对进光量  /  f/4 为基准',28).move_to(DOWN*3.05)
    self.play(FadeIn(bars),FadeIn(barlabels),FadeIn(result),run_time=.7); self.wait(3.0)
    self.next_section('takeaway')
    self.play(FadeOut(head),FadeOut(barlabels),FadeOut(result),FadeOut(bars),run_time=.6)
    final=txt('f/2.8 更亮  ·  f/4 进光更少',36).move_to(UP*2.55)
    foot=txt('其他条件相同  /  约相差一挡',26,MUTED).move_to(DOWN*2.6)
    self.play(FadeIn(final),FadeIn(foot),run_time=.7); self.wait(3)
