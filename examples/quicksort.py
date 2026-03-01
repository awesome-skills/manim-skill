from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import *


@dataclass
class Event:
    array: list[int]
    left: int
    right: int
    pivot_index: int | None
    compare_indices: tuple[int, ...]
    swap_indices: tuple[int, ...]
    sorted_indices: tuple[int, ...]
    message: str
    action: str
    depth: int
    step: int
    comparisons: int
    swaps: int


class QuickSortBars(Scene):
    """
    Cinematic quicksort visualization (Lomuto partition).

    4K render reference:
      manim -pqh --fps 60 --resolution 3840,2160 examples/quicksort.py QuickSortBars
    """

    BAR_WIDTH = 0.48
    BAR_GAP = 0.12
    BASELINE_Y = -2.55
    MAX_BAR_HEIGHT = 3.25
    MESSAGE_FONT_SIZE = 26

    def construct(self) -> None:
        data = [14, 3, 9, 1, 11, 7, 2, 13, 5, 10, 6, 12, 4, 8]
        events = self.build_events(data)
        max_value = max(data)

        self.add(*self.build_background())

        title = Text("Quick Sort", font_size=56, weight=BOLD, color=WHITE).to_edge(UP, buff=0.2)
        subtitle = Text(
            "Lomuto Partition | AI-ready Showcase",
            font_size=24,
            color=GRAY_A,
        ).next_to(title, DOWN, buff=0.08)
        self.play(FadeIn(title, shift=0.15 * DOWN), FadeIn(subtitle, shift=0.15 * DOWN), run_time=1.0)

        bars, value_labels, index_labels = self.build_bars(events[0], len(data), max_value)
        baseline = Line(
            np.array([-6.4, self.BASELINE_Y, 0]),
            np.array([6.4, self.BASELINE_Y, 0]),
            stroke_color=GRAY_B,
            stroke_width=2,
        )

        message = Text(events[0].message, font_size=self.MESSAGE_FONT_SIZE, color=GRAY_A).to_edge(DOWN, buff=0.38)

        legend = self.build_legend()
        legend.to_corner(UR, buff=0.28)

        stats_panel = RoundedRectangle(corner_radius=0.14, width=3.9, height=1.7)
        stats_panel.set_stroke(color=GRAY_C, width=1.5, opacity=0.8)
        stats_panel.set_fill(color="#101827", opacity=0.84)
        stats_panel.to_corner(UL, buff=0.28)
        stats_text = self.build_stats_text(events[0]).move_to(stats_panel.get_center()).align_to(stats_panel, LEFT).shift(
            RIGHT * 0.2
        )

        active_range = self.build_active_range_box(events[0], bars)
        pivot_marker = self.build_pivot_marker(events[0], bars)

        self.play(
            Create(baseline),
            FadeIn(legend, shift=0.1 * UP),
            FadeIn(stats_panel, shift=0.1 * UP),
            FadeIn(stats_text, shift=0.1 * UP),
            LaggedStart(*[Create(bar) for bar in bars], lag_ratio=0.04),
            FadeIn(value_labels),
            FadeIn(index_labels),
            FadeIn(message, shift=0.1 * UP),
            FadeIn(active_range),
            FadeIn(pivot_marker),
            run_time=2.2,
        )

        for event in events[1:]:
            target_bars, target_labels, _ = self.build_bars(event, len(data), max_value)
            target_message = Text(event.message, font_size=self.MESSAGE_FONT_SIZE, color=GRAY_A).to_edge(DOWN, buff=0.38)
            target_stats = self.build_stats_text(event).move_to(stats_text).align_to(stats_panel, LEFT).shift(RIGHT * 0.2)
            target_range = self.build_active_range_box(event, target_bars)
            target_pivot = self.build_pivot_marker(event, target_bars)

            self.play(
                Transform(bars, target_bars),
                Transform(value_labels, target_labels),
                Transform(message, target_message),
                Transform(stats_text, target_stats),
                Transform(active_range, target_range),
                Transform(pivot_marker, target_pivot),
                run_time=self.duration_for(event.action),
            )

            if event.compare_indices:
                highlights = VGroup(*[bars[i] for i in event.compare_indices])
                self.play(Indicate(highlights, color=ORANGE, scale_factor=1.02), run_time=0.18)

            if len(event.swap_indices) == 2:
                left_idx, right_idx = event.swap_indices
                self.play(
                    Flash(bars[left_idx].get_top(), color=RED_C, flash_radius=0.28),
                    Flash(bars[right_idx].get_top(), color=RED_C, flash_radius=0.28),
                    run_time=0.25,
                )

            if event.action == "pivot_fixed" and event.pivot_index is not None:
                self.play(
                    Circumscribe(
                        bars[event.pivot_index],
                        color=GREEN_C,
                        fade_out=True,
                        stroke_width=3,
                    ),
                    run_time=0.26,
                )

        final_badge = Text("Sorted", font_size=48, weight=BOLD, color=GREEN_A).next_to(subtitle, DOWN, buff=0.12)
        complexity = VGroup(
            Text("Average: O(n log n)", font_size=24, color=GRAY_A),
            Text("Worst: O(n^2)", font_size=24, color=GRAY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        complexity.to_edge(DOWN, buff=0.28).shift(UP * 0.28 + LEFT * 4.35)

        self.play(FadeOut(message, shift=0.12 * DOWN), FadeIn(complexity, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(final_badge, scale=0.94), run_time=0.6)
        self.wait(1.2)

    def build_background(self) -> list[Mobject]:
        base = Rectangle(width=config.frame_width, height=config.frame_height)
        base.set_fill(color="#05070f", opacity=1.0)
        base.set_stroke(width=0)

        glow_1 = Circle(radius=3.6).set_fill(color=BLUE_E, opacity=0.16).set_stroke(width=0)
        glow_1.move_to(np.array([-4.4, 2.5, 0]))

        glow_2 = Circle(radius=3.9).set_fill(color=PURPLE_E, opacity=0.11).set_stroke(width=0)
        glow_2.move_to(np.array([4.8, -2.8, 0]))

        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GRAY_E,
                "stroke_opacity": 0.08,
                "stroke_width": 1,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=2,
        )
        grid.scale(0.92)
        return [base, glow_1, glow_2, grid]

    def build_events(self, source: list[int]) -> list[Event]:
        arr = source[:]
        events: list[Event] = []
        sorted_set: set[int] = set()
        step = 0
        comparisons = 0
        swaps = 0

        def snapshot(
            left: int,
            right: int,
            pivot_index: int | None,
            compare_indices: tuple[int, ...],
            swap_indices: tuple[int, ...],
            message: str,
            action: str,
            depth: int,
        ) -> None:
            nonlocal step
            step += 1
            events.append(
                Event(
                    array=arr[:],
                    left=left,
                    right=right,
                    pivot_index=pivot_index,
                    compare_indices=compare_indices,
                    swap_indices=swap_indices,
                    sorted_indices=tuple(sorted(sorted_set)),
                    message=message,
                    action=action,
                    depth=depth,
                    step=step,
                    comparisons=comparisons,
                    swaps=swaps,
                )
            )

        snapshot(0, len(arr) - 1, None, (), (), "Start: unsorted array", "start", 0)

        def quicksort(left: int, right: int, depth: int) -> None:
            nonlocal comparisons, swaps

            if left > right:
                return

            if left == right:
                sorted_set.add(left)
                snapshot(
                    left,
                    right,
                    left,
                    (),
                    (),
                    f"Index {left} is fixed",
                    "single",
                    depth,
                )
                return

            pivot_value = arr[right]
            snapshot(
                left,
                right,
                right,
                (),
                (),
                f"Choose pivot {pivot_value} at index {right}",
                "pick_pivot",
                depth,
            )

            i = left - 1
            for j in range(left, right):
                comparisons += 1
                snapshot(
                    left,
                    right,
                    right,
                    (j,),
                    (),
                    f"Compare a[{j}] = {arr[j]} with pivot {pivot_value}",
                    "compare",
                    depth,
                )

                if arr[j] <= pivot_value:
                    i += 1
                    if i != j:
                        arr[i], arr[j] = arr[j], arr[i]
                        swaps += 1
                        snapshot(
                            left,
                            right,
                            right,
                            (),
                            (i, j),
                            f"Swap index {i} and {j}",
                            "swap",
                            depth,
                        )
                    else:
                        snapshot(
                            left,
                            right,
                            right,
                            (i,),
                            (),
                            f"Keep index {i} in <= pivot region",
                            "keep",
                            depth,
                        )

            pivot_index = i + 1
            if pivot_index != right:
                arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
                swaps += 1
                snapshot(
                    left,
                    right,
                    pivot_index,
                    (),
                    (pivot_index, right),
                    f"Move pivot to index {pivot_index}",
                    "swap",
                    depth,
                )

            sorted_set.add(pivot_index)
            snapshot(
                left,
                right,
                pivot_index,
                (),
                (),
                f"Pivot fixed at index {pivot_index}",
                "pivot_fixed",
                depth,
            )

            quicksort(left, pivot_index - 1, depth + 1)
            quicksort(pivot_index + 1, right, depth + 1)

        quicksort(0, len(arr) - 1, 0)
        snapshot(0, len(arr) - 1, None, (), (), "Array is fully sorted", "done", 0)
        return events

    def build_bars(
        self, event: Event, total: int, max_value: int
    ) -> tuple[VGroup, VGroup, VGroup]:
        bars = VGroup()
        labels = VGroup()
        index_labels = VGroup()

        step = self.BAR_WIDTH + self.BAR_GAP
        center = (total - 1) / 2
        sorted_set = set(event.sorted_indices)
        compare_set = set(event.compare_indices)
        swap_set = set(event.swap_indices)

        for idx, value in enumerate(event.array):
            height = 0.55 + (value / max_value) * self.MAX_BAR_HEIGHT
            color = self.color_for_index(
                idx=idx,
                left=event.left,
                right=event.right,
                pivot_index=event.pivot_index,
                sorted_set=sorted_set,
                compare_set=compare_set,
                swap_set=swap_set,
            )
            x = (idx - center) * step

            bar = RoundedRectangle(
                corner_radius=0.08,
                width=self.BAR_WIDTH,
                height=height,
                stroke_width=1.5,
                stroke_color=WHITE,
                fill_color=color,
                fill_opacity=0.95,
            )
            bar.move_to(np.array([x, self.BASELINE_Y + height / 2, 0]))
            bars.add(bar)

            value_label = Text(str(value), font_size=22, color=WHITE)
            value_label.next_to(bar, UP, buff=0.09)
            labels.add(value_label)

            idx_label = Text(str(idx), font_size=14, color=GRAY_C)
            idx_label.next_to(bar, DOWN, buff=0.09)
            index_labels.add(idx_label)

        return bars, labels, index_labels

    def build_active_range_box(self, event: Event, bars: VGroup) -> VMobject:
        if event.left <= event.right and event.left >= 0 and event.right < len(bars):
            subset = VGroup(*[bars[i] for i in range(event.left, event.right + 1)])
            box = SurroundingRectangle(subset, buff=0.12, corner_radius=0.1)
            box.set_fill(color=BLUE_E, opacity=0.12)
            box.set_stroke(color=BLUE_B, width=2.2, opacity=0.85)
            return box

        hidden = RoundedRectangle(corner_radius=0.02, width=0.01, height=0.01)
        hidden.set_fill(opacity=0)
        hidden.set_stroke(opacity=0)
        return hidden

    def build_pivot_marker(self, event: Event, bars: VGroup) -> VGroup:
        arrow = Arrow(
            start=ORIGIN,
            end=UP * 0.8,
            buff=0,
            max_tip_length_to_length_ratio=0.28,
            stroke_width=4,
            color=YELLOW_B,
        )
        label = Text("pivot", font_size=18, color=YELLOW_A)

        if event.pivot_index is not None and 0 <= event.pivot_index < len(bars):
            target = bars[event.pivot_index]
            arrow.put_start_and_end_on(
                target.get_top() + UP * 0.65,
                target.get_top() + UP * 0.12,
            )
            label.next_to(arrow, UP, buff=0.03)
        else:
            arrow.set_opacity(0)
            label.set_opacity(0)
            arrow.move_to(np.array([0, 3.6, 0]))
            label.move_to(np.array([0, 3.9, 0]))

        return VGroup(arrow, label)

    def build_legend(self) -> VGroup:
        def item(color: ManimColor, label: str) -> VGroup:
            swatch = Square(side_length=0.2)
            swatch.set_fill(color, opacity=1.0)
            swatch.set_stroke(WHITE, width=0.8, opacity=0.9)
            text = Text(label, font_size=17, color=GRAY_A)
            row = VGroup(swatch, text).arrange(RIGHT, buff=0.12)
            return row

        rows = VGroup(
            item(BLUE_C, "active partition"),
            item(YELLOW_D, "pivot"),
            item(ORANGE, "comparison"),
            item(RED_C, "swap"),
            item(GREEN_C, "sorted"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        panel = RoundedRectangle(corner_radius=0.12, width=2.95, height=1.72)
        panel.set_stroke(color=GRAY_C, width=1.2, opacity=0.8)
        panel.set_fill(color="#101827", opacity=0.84)
        rows.move_to(panel.get_center()).align_to(panel, LEFT).shift(RIGHT * 0.18)
        return VGroup(panel, rows)

    @staticmethod
    def build_stats_text(event: Event) -> VGroup:
        lines = VGroup(
            Text(f"step: {event.step}", font_size=17, color=GRAY_A),
            Text(f"depth: {event.depth}", font_size=17, color=GRAY_A),
            Text(f"range: [{event.left}, {event.right}]", font_size=17, color=GRAY_A),
            Text(f"comparisons: {event.comparisons}", font_size=17, color=GRAY_A),
            Text(f"swaps: {event.swaps}", font_size=17, color=GRAY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        return lines

    @staticmethod
    def duration_for(action: str) -> float:
        durations = {
            "start": 0.4,
            "pick_pivot": 0.52,
            "compare": 0.3,
            "swap": 0.46,
            "keep": 0.28,
            "pivot_fixed": 0.5,
            "single": 0.34,
            "done": 0.82,
        }
        return durations.get(action, 0.34)

    @staticmethod
    def color_for_index(
        idx: int,
        left: int,
        right: int,
        pivot_index: int | None,
        sorted_set: set[int],
        compare_set: set[int],
        swap_set: set[int],
    ) -> ParsableManimColor:
        if idx in sorted_set:
            return GREEN_C
        if idx in swap_set:
            return RED_C
        if pivot_index is not None and idx == pivot_index:
            return YELLOW_D
        if idx in compare_set:
            return ORANGE
        if left <= idx <= right:
            return BLUE_C
        return GRAY_D
