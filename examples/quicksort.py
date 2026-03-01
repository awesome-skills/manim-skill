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


class QuickSortBars(Scene):
    """Quicksort visualization with bar colors for partition state."""

    BAR_WIDTH = 0.54
    BAR_GAP = 0.14
    BASELINE_Y = -2.7
    MAX_BAR_HEIGHT = 4.2

    def construct(self) -> None:
        data = [8, 3, 1, 7, 0, 10, 2, 6, 4, 5, 9]
        events = self.build_events(data)
        max_value = max(data)

        title = Text("Quick Sort (Lomuto Partition)", font_size=38).to_edge(UP)
        self.play(Write(title), run_time=0.8)

        bars, labels, index_labels = self.build_bars(events[0], len(data), max_value)
        message = Text(events[0].message, font_size=28).to_edge(DOWN)

        self.play(
            LaggedStart(*[Create(bar) for bar in bars], lag_ratio=0.05),
            FadeIn(labels),
            FadeIn(index_labels),
            FadeIn(message),
            run_time=1.8,
        )

        for event in events[1:]:
            target_bars, target_labels, _ = self.build_bars(event, len(data), max_value)
            target_message = Text(event.message, font_size=28).to_edge(DOWN)
            self.play(
                Transform(bars, target_bars),
                Transform(labels, target_labels),
                Transform(message, target_message),
                run_time=0.38,
            )

        self.wait(1.2)

    def build_events(self, source: list[int]) -> list[Event]:
        arr = source[:]
        events: list[Event] = []
        sorted_set: set[int] = set()

        def snapshot(
            left: int,
            right: int,
            pivot_index: int | None,
            compare_indices: tuple[int, ...],
            swap_indices: tuple[int, ...],
            message: str,
        ) -> None:
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
                )
            )

        snapshot(0, len(arr) - 1, None, (), (), "Unsorted array")

        def quicksort(left: int, right: int) -> None:
            if left > right:
                return

            if left == right:
                sorted_set.add(left)
                snapshot(left, right, left, (), (), f"Index {left} is fixed")
                return

            pivot_value = arr[right]
            snapshot(
                left,
                right,
                right,
                (),
                (),
                f"Pick pivot {pivot_value} (index {right})",
            )

            i = left - 1
            for j in range(left, right):
                snapshot(
                    left,
                    right,
                    right,
                    (j,),
                    (),
                    f"Compare {arr[j]} <= {pivot_value}",
                )
                if arr[j] <= pivot_value:
                    i += 1
                    if i != j:
                        arr[i], arr[j] = arr[j], arr[i]
                        snapshot(
                            left,
                            right,
                            right,
                            (),
                            (i, j),
                            f"Swap index {i} and {j}",
                        )
                    else:
                        snapshot(
                            left,
                            right,
                            right,
                            (i,),
                            (),
                            f"Keep {arr[i]} in <= pivot region",
                        )

            pivot_index = i + 1
            if pivot_index != right:
                arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
                snapshot(
                    left,
                    right,
                    pivot_index,
                    (),
                    (pivot_index, right),
                    f"Move pivot to index {pivot_index}",
                )

            sorted_set.add(pivot_index)
            snapshot(
                left,
                right,
                pivot_index,
                (),
                (),
                f"Pivot fixed at index {pivot_index}",
            )

            quicksort(left, pivot_index - 1)
            quicksort(pivot_index + 1, right)

        quicksort(0, len(arr) - 1)
        snapshot(0, len(arr) - 1, None, (), (), "Array is fully sorted")
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

            bar = Rectangle(
                width=self.BAR_WIDTH,
                height=height,
                stroke_width=1.4,
                stroke_color=WHITE,
                fill_color=color,
                fill_opacity=0.96,
            )
            bar.move_to(np.array([x, self.BASELINE_Y + height / 2, 0]))
            bars.add(bar)

            value_label = Text(str(value), font_size=24, color=WHITE)
            value_label.next_to(bar, UP, buff=0.08)
            labels.add(value_label)

            idx_label = Text(str(idx), font_size=14, color=GRAY_B)
            idx_label.next_to(bar, DOWN, buff=0.08)
            index_labels.add(idx_label)

        return bars, labels, index_labels

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
            return YELLOW_C
        if idx in compare_set:
            return ORANGE
        if left <= idx <= right:
            return BLUE_D
        return GRAY_D
