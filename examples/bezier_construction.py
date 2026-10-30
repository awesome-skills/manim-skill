"""Original geometric study: a quadratic curve from repeated linear interpolation."""
import numpy as np
from manim import (Scene, Text, Line, Dot, VGroup, VMobject, ValueTracker,
                   DecimalNumber, FadeIn, FadeOut, Create, always_redraw, linear, LEFT)


def quadratic_construction(points, t):
    p = np.asarray(points, dtype=float)
    q = (1-t)*p[:-1] + t*p[1:]
    return q, (1-t)*q[0] + t*q[1]


class BezierConstruction(Scene):
    def construct(self):
        paper, ink, quiet, blue = '#EBE9A0', '#24352C', '#777B50', '#2456AF'
        self.camera.background_color = paper
        def text(s, size=30, color=ink):
            return Text(s, font='sans-serif', warn_missing_font=False, font_size=size, color=color)
        def left(m, y):return m.move_to([-6.0,y,0],aligned_edge=LEFT)
        eyebrow=left(text('CURVE STUDY / 01',23,quiet),3.35)
        title=left(text('Straight\nto curved.',61),1.7)
        step=left(text('Take the same fraction\non both guide lines.',28),-.3)
        self.add(eyebrow,title)
        points=np.array([[-.6,-1.7,0],[2.3,1.75,0],[5.8,-1.7,0]])
        guides=VGroup(*[Line(points[i],points[i+1],color=quiet,stroke_width=2) for i in range(2)])
        anchors=VGroup(*[Dot(p,radius=.07,color=ink) for p in points])
        names=VGroup(*[text(s,27,quiet).move_to(p+[0,.35 if i==1 else -.4,0]) for i,(s,p) in enumerate(zip(['A','B','C'],points))])
        self.play(Create(guides),FadeIn(anchors),FadeIn(names),FadeIn(step),run_time=1)
        t=ValueTracker(.5)
        def q():return quadratic_construction(points,t.get_value())[0]
        moving=always_redraw(lambda:VGroup(*[Dot(p,radius=.10,color=blue) for p in q()]))
        fraction=left(text('FRACTION',23,quiet),-1.6)
        class Numeral(Text):
            def __init__(self, value, **kwargs):
                super().__init__(value, font='serif', warn_missing_font=False, **kwargs)
        number=DecimalNumber(.5,num_decimal_places=2,font_size=64,color=ink,mob_class=Numeral)
        number.add_updater(lambda m:left(m.set_value(t.get_value()),-2.35))
        self.next_section('first_interpolation')
        self.play(FadeIn(moving),FadeIn(fraction),FadeIn(number),run_time=.7)
        self.wait(2)
        bridge=always_redraw(lambda:Line(*q(),color=blue,stroke_width=3))
        result=always_redraw(lambda:Dot(quadratic_construction(points,t.get_value())[1],radius=.14,color=ink))
        self.play(FadeOut(step),run_time=.25)
        step=left(text('Repeat on the line\nbetween those two points.',28),-.3)
        self.play(Create(bridge),FadeIn(step),run_time=.8)
        self.play(FadeIn(result),run_time=.4)
        self.wait(2)
        self.next_section('trace')
        self.play(t.animate.set_value(0),run_time=1.5)
        self.play(FadeOut(step),run_time=.25)
        step=left(text('Change the fraction.\nThe final point traces a curve.',26),-.3)
        self.play(FadeIn(step),run_time=.4)
        trace=VMobject(color=ink,stroke_width=5)
        def redraw(m):
            ts=np.linspace(0,max(t.get_value(),1e-6),181)
            m.set_points_as_corners([quadratic_construction(points,a)[1] for a in ts])
        trace.add_updater(redraw)
        self.add(trace)
        result.set_z_index(3)
        self.play(t.animate.set_value(1),run_time=6,rate_func=linear)
        self.wait(.8)
        self.next_section('resolve')
        # Freeze first, then fade construction geometry without updater interference.
        for m in [moving,bridge,result,trace,number]:m.clear_updaters()
        self.play(FadeOut(moving),FadeOut(bridge),FadeOut(result),FadeOut(step),run_time=.4)
        final=left(text('A quadratic\nBézier curve.',35),-.3)
        self.play(FadeIn(final),run_time=.5)
        self.wait(2)
