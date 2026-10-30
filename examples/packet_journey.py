"""Original cause-and-effect diagram, recomposed for portrait or landscape.

Portrait: --resolution 720,1280; initialize a matching camera before constructing.
"""
from manim import (
    Arrow, Circle, Create, FadeIn, FadeOut, Line, MoveAlongPath,
    RoundedRectangle, Scene, Text, VGroup, config, tempconfig,
)


class PacketJourney(Scene):
    def __init__(self, **kwargs):
        # Cairo preserves frame width when adjusting to pixel aspect ratio.
        # Set it before Scene creates the camera; restore global config afterward.
        aspect = config.pixel_width / config.pixel_height
        with tempconfig({"frame_width": config.frame_height * aspect}):
            super().__init__(**kwargs)

    def construct(self):
        def text(words, **kwargs):
            return Text(words, font="sans-serif", warn_missing_font=False, **kwargs)

        bg, ink, muted, accent = "#F4F1E9", "#263635", "#61716B", "#176D60"
        self.camera.background_color = bg
        portrait = self.camera.frame_width < self.camera.frame_height
        width = self.camera.frame_width
        title = text("A request, step by step", color=ink, font_size=40 if not portrait else 28)
        title.scale_to_fit_width(min(title.width, width - 0.7)).move_to([0, 3.12, 0])
        subtitle = text("Arrival triggers the next action.", color=muted, font_size=23 if not portrait else 19)
        subtitle.scale_to_fit_width(min(subtitle.width, width - 0.7)).move_to([0, 2.55, 0])
        self.add(title, subtitle)
        positions = [[0, 1.4, 0], [0, -0.2, 0], [0, -1.8, 0]] if portrait else [
            [-4.3, 0.25, 0], [0, 0.25, 0], [4.3, 0.25, 0]]
        names = ["Client", "Validate", "Store"]
        boxes, nodes = [], VGroup()
        for name, position in zip(names, positions):
            box = RoundedRectangle(width=2.5, height=0.9 if portrait else 1.25,
                                   corner_radius=0.14, stroke_width=2, stroke_color=muted,
                                   fill_color=bg, fill_opacity=1).move_to(position)
            boxes.append(box)
            nodes.add(VGroup(box, text(name, color=ink, font_size=25).move_to(position)))
        links = VGroup()
        for a, b in zip(boxes, boxes[1:]):
            start, end = (a.get_bottom(), b.get_top()) if portrait else (a.get_right(), b.get_left())
            links.add(Arrow(start, end, buff=0.12, color=muted, stroke_width=2,
                            max_tip_length_to_length_ratio=0.12))
        self.next_section("route")
        self.play(FadeIn(nodes), Create(links), run_time=1)
        self.wait(0.8)
        self.next_section("request")
        self.play(boxes[0].animate.set_stroke(accent, width=4), run_time=0.3)
        token = Circle(radius=0.09, fill_color=accent, fill_opacity=1, stroke_width=0)
        self.wait(0.7)
        captions = ["1 / Check the request", "2 / Save the result"]
        for i, link in enumerate(links):
            self.next_section(f"arrival_{i + 1}")
            token.move_to(link.get_start())
            self.play(FadeIn(token), run_time=0.15)
            self.play(MoveAlongPath(token, Line(link.get_start(), link.get_end())), run_time=1.1)
            # Destination emphasis begins only after the packet arrives.
            self.play(FadeOut(token), boxes[i + 1].animate.set_stroke(accent, width=4), run_time=0.25)
            caption = text(captions[i], font_size=24 if not portrait else 21, color=accent)
            caption.move_to([0, -2.9, 0])
            self.play(FadeIn(caption), run_time=0.3)
            self.wait(1.2)
            self.play(FadeOut(caption), run_time=0.25)
        self.next_section("complete")
        caption = text("Received. Checked. Stored.", color=accent, font_size=28 if not portrait else 22)
        caption.scale_to_fit_width(min(caption.width, width - 0.7)).move_to([0, -2.9, 0])
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(2)
