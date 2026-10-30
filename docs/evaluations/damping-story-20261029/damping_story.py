"""Three-beat physical explanation with shared scales and analytic state."""
import numpy as np
from manim import (Scene, Text, Line, Square, VMobject, VGroup, ValueTracker,
                   Rectangle, FadeIn, FadeOut, always_redraw, linear, LEFT)


def spring_state(t, damping, omega=2.4, amplitude=1.35):
    """Underdamped oscillator released from rest; mass=1, stiffness=omega²."""
    t = np.asarray(t)
    q = np.sqrt(1 - damping**2)
    decay = np.exp(-damping * omega * t)
    x = amplitude * decay * (np.cos(omega*q*t) + damping/q*np.sin(omega*q*t))
    v = -amplitude * omega/q * decay * np.sin(omega*q*t)
    energy = (v*v + omega*omega*x*x)/(omega*omega*amplitude*amplitude)
    return x, v, energy


class DampingStory(Scene):
    def construct(self):
        paper, ink, muted = '#F1E9E3', '#293543', '#77726E'
        coral, teal = '#B44E36', '#277870'
        self.camera.background_color = paper
        def text(s,size=32,color=ink):
            return Text(s,font='sans-serif',warn_missing_font=False,font_size=size,color=color)
        def left(m,x,y):return m.move_to([x,y,0],aligned_edge=LEFT)
        chapter=left(text('01 / THE RELEASE',24,muted),-6.1,3.45)
        title=left(text('Without damping, motion persists.',46),-6.1,2.75)
        self.add(chapter,title)
        clock=ValueTracker(0)
        def assembly(y,damping,color):
            wall=Line([-5.6,y-.45,0],[-5.6,y+.45,0],color=muted,stroke_width=4)
            eq=Line([-1.25,y-.65,0],[-1.25,y+.65,0],color=muted,stroke_width=1)
            def live():
                x,_,_=spring_state(clock.get_value(),damping)
                cx=-1.25+float(x)
                block=Square(side_length=.7,color=color,fill_color=color,fill_opacity=1,stroke_width=0).move_to([cx,y,0])
                xs=np.linspace(-5.45,cx-.35,29)
                pts=[[xx,y+(0 if i in (0,28) else .17*(-1)**i),0] for i,xx in enumerate(xs)]
                coil=VMobject(color=color,stroke_width=2.8).set_points_as_corners(pts)
                return VGroup(coil,block)
            return VGroup(wall,eq,always_redraw(live))
        top=assembly(.55,0,coral)
        top_name=left(text('NO DAMPING',28,coral),-5.6,1.35)
        note=text('Release from rest. Watch it cross the resting position.',30).move_to([0,-2.8,0])
        self.play(FadeIn(top),FadeIn(top_name),FadeIn(note),run_time=.7)
        self.wait(.8)
        self.next_section('release')
        self.play(clock.animate.set_value(5),run_time=5,rate_func=linear)
        self.wait(.5)
        self.play(FadeOut(top),FadeOut(top_name),FadeOut(note),FadeOut(title),FadeOut(chapter),run_time=.3)
        clock.set_value(0)
        chapter=left(text('02 / THE COMPARISON',24,muted),-6.1,3.45)
        title=left(text('Same spring. Add damping.',46),-6.1,2.75)
        bottom=assembly(-1.25,.32,teal)
        bottom_name=left(text('WITH DAMPING',28,teal),-5.6,-.45)
        energy_title=left(text('Energy remaining',28,muted),2.8,1.35)
        tracks=VGroup()
        for y,d,color in [(.55,0,coral),(-1.25,.32,teal)]:
            track=Rectangle(width=2.8,height=.16,stroke_width=0,fill_color=muted,fill_opacity=.15).move_to([4.2,y,0])
            def energy_bar(y=y,d=d,color=color):
                fraction=float(spring_state(clock.get_value(),d)[2])
                return Rectangle(width=max(1e-6,2.8*fraction),height=.16,stroke_width=0,fill_color=color,fill_opacity=1).move_to([2.8,y,0],aligned_edge=LEFT)
            tracks.add(track,always_redraw(energy_bar))
        note=text('Equal mass, stiffness and starting displacement.',30).move_to([0,-2.8,0])
        self.play(FadeIn(chapter),FadeIn(title),FadeIn(top),FadeIn(top_name),FadeIn(bottom),FadeIn(bottom_name),FadeIn(tracks),FadeIn(energy_title),FadeIn(note),run_time=.8)
        self.wait(1.2)
        self.next_section('compare')
        self.play(clock.animate.set_value(10),run_time=10,rate_func=linear)
        self.wait(.5)
        self.play(FadeOut(chapter),FadeOut(title),FadeOut(note),run_time=.3)
        chapter=left(text('03 / AT TEN SECONDS',24,muted),-6.1,3.45)
        title=left(text('Damping removes mechanical energy.',43),-6.1,2.75)
        note=text('The ideal spring keeps moving. The damped one settles.',30).move_to([0,-2.8,0])
        self.play(FadeIn(chapter),FadeIn(title),FadeIn(note),run_time=.5)
        self.wait(3)
        for mob in [top,bottom,tracks]:mob.clear_updaters(recursive=True)
