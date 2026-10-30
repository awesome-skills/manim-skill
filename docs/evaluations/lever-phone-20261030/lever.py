from manim import *
import numpy as np

BG='#101820'; INK='#F5F1E8'; DIM='#A7B5BC'; GOLD='#EABF78'; BLUE='#8CC9D3'; FONT='Hiragino Sans GB'
class Lever(Scene):
 def construct(self):
  self.camera.background_color=BG
  def text(s,size=36,color=INK): return Text(s,font=FONT,font_size=size,color=color)
  def cap(s): return text(s,36).move_to([0,-3.35,0])
  self.next_section('model')
  title=text('为什么离支点越远，越省力？',42).move_to([0,3.35,0])
  model=text('忽略杆重与摩擦 · 竖直施力',30,DIM).move_to([0,2.72,0])
  self.play(FadeIn(title),run_time=.7); self.wait(.6)
  self.play(FadeIn(model),run_time=.5)
  # One model: load force W = 1, load arm a = 2, effort arm r ∈ [2,4].
  # Equilibrium W*a = F*r; the arrow length is proportional to the force.
  px=-1.2; y=.45; a=2.; W=1.; scale=1.15; unit=1.3
  r=ValueTracker(2.)
  beam=Line([px-unit*2.55,y,0],[px+unit*4.6,y,0],color=INK,stroke_width=13)
  pivot=Dot([px,y,0],radius=.085,color=GOLD)
  support=Polygon([px,y-.1,0],[px-.48,y-1.0,0],[px+.48,y-1.0,0],fill_color=DIM,fill_opacity=1,stroke_width=0)
  base=Line([px-.75,y-1.02,0],[px+.75,y-1.02,0],color=DIM,stroke_width=3)
  pivot_label=text('支点',30,DIM).next_to(base,DOWN,buff=.1)
  load=RoundedRectangle(width=1.1,height=.8,corner_radius=.08,fill_color=BLUE,fill_opacity=1,stroke_width=0).move_to([px-unit*a,y+.46,0])
  load_label=text('重物',32,BG).move_to(load)
  weight=Arrow([px-unit*a,y+.8+scale,0],[px-unit*a,y+.8,0],buff=0,color=BLUE,stroke_width=7,max_tip_length_to_length_ratio=.19)
  def effort():
   length=scale*W*a/r.get_value(); x=px+unit*r.get_value()
   return Arrow([x,y+.12+length,0],[x,y+.12,0],buff=0,color=GOLD,stroke_width=7,max_tip_length_to_length_ratio=.26)
  effort_arrow=always_redraw(effort)
  effort_label=always_redraw(lambda:text('施力',32,GOLD).next_to(effort_arrow,UP,buff=.1))
  self.play(Create(beam),FadeIn(support),Create(base),FadeIn(pivot),FadeIn(pivot_label),FadeIn(load),FadeIn(load_label),run_time=1.1)
  c=cap('力臂相等，平衡时力也相等')
  self.play(GrowArrow(weight),FadeIn(effort_arrow),FadeIn(effort_label),FadeIn(c),run_time=.8)
  # Separate dimension channels, below the support, with endpoints tied to model geometry.
  y1=-1.28; y2=-2.15
  def dim(x0,x1,yy,color):
   return VGroup(Line([x0,yy,0],[x1,yy,0],color=color,stroke_width=3),Line([x0,yy-.1,0],[x0,yy+.1,0],color=color,stroke_width=3),Line([x1,yy-.1,0],[x1,yy+.1,0],color=color,stroke_width=3))
  # The left dimension is kept left of the pivot; labels sit in their own row.
  leftdim=dim(px-unit*a,px,y1,BLUE)
  leftlabel=text('重物臂',32,BLUE).move_to([px-unit*a/2,y1-.34,0])
  rightdim=always_redraw(lambda:dim(px,px+unit*r.get_value(),y2,GOLD))
  rightlabel=always_redraw(lambda:text('用力臂',32,GOLD).move_to([px+unit*r.get_value()/2,y2-.34,0]))
  self.play(Create(leftdim),FadeIn(leftlabel),FadeIn(rightdim),FadeIn(rightlabel),run_time=.7); self.wait(2)
  self.next_section('move_and_balance')
  self.play(FadeOut(c),run_time=.3)
  c=cap('向外移，保持平衡的力逐渐减小')
  self.play(FadeIn(c),run_time=.4)
  self.wait(.5)
  self.play(r.animate.set_value(4),run_time=5,rate_func=linear)
  self.wait(1)
  self.next_section('comparison')
  self.play(FadeOut(c),run_time=.3)
  c=cap('力臂变成 2 倍，力只需一半')
  self.play(FadeIn(c),run_time=.5); self.wait(2.3)
  self.next_section('conclusion')
  self.play(FadeOut(title),FadeOut(c),run_time=.4)
  conclusion=text('力 × 力臂 = 转动作用',42).move_to([0,3.35,0])
  c=cap('相同转动作用，力臂越长越省力')
  self.play(FadeIn(conclusion),FadeIn(c),run_time=.6); self.wait(3)
