"""Portable Cairo examples; OpenGL needs a separate renderer-specific check."""
from manim import *


class CameraFocus(MovingCameraScene):
    def construct(self):
        left = Square(color=BLUE).shift(LEFT * 3)
        right = Circle(color=GREEN).shift(RIGHT * 3)
        self.add(left, right)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(right).set(width=4))
        self.wait(0.5)
        self.play(Restore(self.camera.frame))
        self.wait(0.5)


class Orbit3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes()
        sphere = Sphere(radius=1, resolution=(12, 24), color=BLUE)
        title = Text("3D orbit", font_size=30).to_corner(UL)
        self.add(axes, sphere)
        self.add_fixed_in_frame_mobjects(title)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(2)
        self.stop_ambient_camera_rotation()
