"""An original continuous handoff: one orbit becomes a record of its height."""
import numpy as np
from manim import (
    Scene, Text, Circle, Dot, Line, VGroup, ValueTracker, VMobject,
    FadeIn, FadeOut, Create, always_redraw, linear, LEFT,
)


class CircleToWave(Scene):
    def construct(self):
        ground, ink, quiet, accent = '#20272C', '#EFE9DD', '#788589', '#E7AE71'
        self.camera.background_color = ground
        def label(s, size=32, color=ink):
            return Text(s, font='sans-serif', warn_missing_font=False, font_size=size, color=color)
        def heading(s):
            return label(s, 47).move_to([-6.1, 2.9, 0], aligned_edge=LEFT)
        title = heading('One orbit. A changing height.')
        kicker = label('MOTION / A CONTINUOUS VIEW', 23, quiet).move_to([-6.1,3.55,0],aligned_edge=LEFT)
        self.add(title,kicker)
        phase, center_x = ValueTracker(0), ValueTracker(0)
        radius, base = 1.5, -.25
        def center():return np.array([center_x.get_value(),base,0])
        def orbit_point():
            a=phase.get_value()
            return center()+radius*np.array([np.cos(a),np.sin(a),0])
        orbit=Circle(radius=radius,color=quiet,stroke_width=2).move_to(center())
        orbit.add_updater(lambda m:m.move_to(center()))
        spoke=always_redraw(lambda:Line(center(),orbit_point(),color=accent,stroke_width=2))
        dot=Dot(radius=.11,color=accent).add_updater(lambda m:m.move_to(orbit_point()))
        axis=always_redraw(lambda:Line(center()+[-1.85,0,0],center()+[1.85,0,0],color=quiet,stroke_width=1))
        self.play(Create(orbit),FadeIn(axis),FadeIn(spoke),FadeIn(dot),run_time=.8)
        self.next_section('orbit')
        self.play(phase.animate.set_value(2*np.pi),run_time=3,rate_func=linear)
        self.wait(.6)
        self.next_section('handoff')
        self.play(FadeOut(title),run_time=.25)
        # The center is the shared parent-like transform. Phase is held still.
        self.play(center_x.animate.set_value(-4.25),run_time=1.4)
        title=heading('Keep the height. Record the phase.')
        self.play(FadeIn(title),run_time=.4)
        phase.set_value(0)  # Same position at the completed revolution.
        start_x, length = -1.65, 7.25
        def wave_point(t):return np.array([start_x+length*t/(2*np.pi),base+radius*np.sin(t),0])
        wave_axis=Line([start_x,base,0],[start_x+length+.25,base,0],color=quiet,stroke_width=1)
        ends=VGroup(label('0',26,quiet).move_to([start_x,-2.15,0]),label('one turn',26,quiet).move_to([start_x+length,-2.15,0]))
        bridge=always_redraw(lambda:Line(orbit_point(),wave_point(phase.get_value()),color=accent,stroke_width=2.5,stroke_opacity=.85))
        trace=VMobject(color=accent,stroke_width=4)
        def update_trace(m):
            t=phase.get_value()
            # Fixed samples of the analytic curve: no dependence on prior frames.
            ts=np.linspace(0,max(t,1e-6),max(2,int(t*60)+2))
            m.set_points_as_corners([wave_point(a) for a in ts])
        trace.add_updater(update_trace)
        head=Dot(radius=.085,color=accent).add_updater(lambda m:m.move_to(wave_point(phase.get_value())))
        note=label('The two points share the same vertical coordinate.',30).move_to([0,-3.1,0])
        self.play(Create(wave_axis),FadeIn(ends),FadeIn(bridge),FadeIn(head),FadeIn(note),run_time=.7)
        self.add(trace)
        self.next_section('record_height')
        self.play(phase.animate.set_value(2*np.pi),run_time=6,rate_func=linear)
        self.wait(.8)
        self.play(FadeOut(note),run_time=.25)
        result=label('Circular motion, seen as a sine wave.',36).move_to([0,-3.1,0])
        self.play(FadeIn(result),run_time=.45)
        self.wait(2)
        for mob in [orbit,spoke,dot,axis,bridge,trace,head]:mob.clear_updaters()
