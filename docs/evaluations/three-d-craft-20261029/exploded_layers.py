"""An original opaque 3D exploded view with screen-fixed annotations."""
from manim import (ThreeDScene, Text, Prism, VGroup, FadeIn, DEGREES, LEFT)


class ExplodedLayers(ThreeDScene):
    def construct(self):
        ground, ink, quiet = '#1D2730', '#EDE6DA', '#ADBBC0'
        colors = ['#6FAEB5', '#D4AD73', '#BE7867']
        self.camera.background_color = ground
        self.set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES, zoom=1)

        def text(s, size=30, color=ink):
            return Text(s, font='sans-serif', warn_missing_font=False, font_size=size, color=color)

        title = text('One stack. Three equal layers.', 45).move_to([-6.0, 3.1, 0], aligned_edge=LEFT)
        note = text('Only the spacing changes.', 30, quiet).move_to([0, -3.35, 0])
        legend = VGroup(*[text(s, 30, c).move_to([-4.7, y, 0])
                         for s,c,y in zip(['Top', 'Middle', 'Bottom'], colors[::-1], [1, 0, -1])])
        self.add_fixed_in_frame_mobjects(title, note, legend)
        layers = VGroup(*[
            Prism(dimensions=[3.4, 2.2, .5], fill_color=c, fill_opacity=1,
                  stroke_color=ground, stroke_width=1).move_to([0, 0, z])
            for c,z in zip(colors, [-.52, 0, .52])
        ])
        self.next_section('assembled')
        self.play(FadeIn(layers), run_time=.8)
        self.wait(1.6)
        self.next_section('separate')
        self.play(layers[0].animate.shift([0,0,-.98]),
                  layers[2].animate.shift([0,0,.98]), run_time=2)
        self.wait(1.5)
        self.next_section('inspect_depth')
        self.move_camera(theta=-15*DEGREES, run_time=2)
        self.wait(1.5)
        self.next_section('reassemble')
        self.play(layers[0].animate.shift([0,0,.98]),
                  layers[2].animate.shift([0,0,-.98]), run_time=1.8)
        self.wait(.7)
        self.move_camera(theta=-45*DEGREES, run_time=1.5)
        self.wait(2)
