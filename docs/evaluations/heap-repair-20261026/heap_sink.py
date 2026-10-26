"""Silent Chinese max-heap root removal and sift-down, Manim CE 0.22.
Render: python -m manim render -qm --renderer cairo --format mp4 heap_sink.py HeapSink
"""
from manim import *
import numpy as np
BG, INK, MUTED = '#101823', '#F0F4F8', '#93A4B5'
EDGE, CYAN, AMBER, RED, GREEN = '#45596D', '#5AD7E8', '#FFCD69', '#FF8686', '#9BE0AB'
FONT = 'Hiragino Sans GB'

class HeapSink(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text('取走最大值后，为什么要下沉？',font=FONT,font_size=37,color=INK).move_to([0,3.35,0])
        caption = Text('最大堆：每个父节点 ≥ 它的孩子',font=FONT,font_size=28,color=INK).move_to([0,2.55,0])
        points = [np.array(p,dtype=float) for p in [(0,1.4,0),(-2,.05,0),(2,.05,0),(-3,-1.3,0),(-1,-1.3,0),(1,-1.3,0),(3,-1.3,0)]]
        ap = [np.array([-3.6+1.2*i,-2.65,0]) for i in range(7)]
        values = [90,70,80,40,60,50,30]
        edges = {i:Line(points[(i-1)//2],points[i],buff=.33,color=EDGE,stroke_width=3) for i in range(1,7)}
        nodes = [Circle(radius=.33,color=EDGE,stroke_width=3,fill_color=BG,fill_opacity=1).move_to(p) for p in points]
        labels = [Text(str(v),font=FONT,font_size=28,color=INK).move_to(p) for v,p in zip(values,points)]
        indices = [Text(str(i),font=FONT,font_size=15,color=MUTED).move_to(p+np.array([.43,.25,0])) for i,p in enumerate(points)]
        cells = [Square(side_length=.82,color=EDGE,stroke_width=2).move_to(p) for p in ap]
        arr = [Text(str(v),font=FONT,font_size=27,color=INK).move_to(p) for v,p in zip(values,ap)]
        ai = [Text(str(i),font=FONT,font_size=18,color=MUTED).move_to(p+DOWN*.63) for i,p in enumerate(ap)]
        tree_name=Text('树',font=FONT,font_size=22,color=MUTED).move_to([-4.6,.1,0])
        arr_name=Text('数组',font=FONT,font_size=22,color=MUTED).move_to([-5,-2.65,0])
        def say(s):
            nonlocal caption
            new=Text(s,font=FONT,font_size=28,color=INK).move_to([0,2.55,0])
            self.play(FadeOut(caption),FadeIn(new),run_time=.3)
            caption=new
        def mark(ids,color):
            self.play(*[m.animate.set_stroke(color) for i in ids for m in (nodes[i],cells[i])],run_time=.4)
        def swap(a,b,duration=1):
            self.play(labels[a].animate(path_arc=PI/3).move_to(points[b]),labels[b].animate(path_arc=PI/3).move_to(points[a]),MoveAlongPath(arr[a],CubicBezier(ap[a],ap[a]+UP*.65,ap[b]+UP*.65,ap[b])),MoveAlongPath(arr[b],CubicBezier(ap[b],ap[b]+UP*1.15,ap[a]+UP*1.15,ap[a])),run_time=duration)
            labels[a],labels[b]=labels[b],labels[a]
            arr[a],arr[b]=arr[b],arr[a]
            values[a],values[b]=values[b],values[a]
        self.next_section('establish_correspondence')
        self.play(FadeIn(title),FadeIn(caption),FadeIn(VGroup(*edges.values(),*nodes,*labels,*indices,*cells,*arr,*ai,tree_name,arr_name)),run_time=1)
        self.wait(1.3)
        say('树与数组：相同的索引，对应相同的值')
        mark([0,6],CYAN)
        self.wait(1)
        self.next_section('remove_and_replace')
        say('取走堆顶 90，把最后的 30 补到根')
        self.play(labels[0].animate.shift(UP*.55).set_opacity(0),arr[0].animate.shift(UP*.45).set_opacity(0),run_time=.6)
        self.remove(labels[0],arr[0])
        self.play(MoveAlongPath(labels[6],CubicBezier(points[6],np.array([4.,.4,0]),np.array([2.4,2.,0]),points[0])),MoveAlongPath(arr[6],CubicBezier(ap[6],ap[6]+UP*.9,ap[0]+UP*.9,ap[0])),FadeOut(nodes[6]),FadeOut(indices[6]),FadeOut(edges[6]),FadeOut(cells[6]),FadeOut(ai[6]),run_time=1)
        labels[0],arr[0],values[0]=labels[6],arr[6],values[6]
        self.play(labels[0].animate.set_color(AMBER),arr[0].animate.set_color(AMBER),run_time=.3)
        self.wait(.9)
        self.next_section('local_violation')
        say('根变小了：30 < 70，也 < 80')
        mark([0],RED)
        self.play(edges[1].animate.set_color(RED),edges[2].animate.set_color(RED),run_time=.4)
        self.wait(1.3)
        self.next_section('choose_larger_child')
        say('先选较大的孩子 80；换上去才能压住两边')
        mark([2],CYAN)
        self.wait(1)
        swap(0,2,1.1)
        self.play(nodes[0].animate.set_stroke(GREEN),cells[0].animate.set_stroke(GREEN),edges[1].animate.set_color(EDGE),edges[2].animate.set_color(EDGE),run_time=.3)
        self.wait(.8)
        self.next_section('continue_downward')
        say('继续沿着 30 往下看：30 < 50，再交换')
        mark([2],RED)
        mark([5],CYAN)
        self.play(edges[5].animate.set_color(RED),run_time=.3)
        self.wait(.8)
        swap(2,5,1)
        self.wait(.6)
        self.next_section('restored')
        assert values[:6]==[80,70,50,40,60,30]
        assert all(values[(i-1)//2]>=values[i] for i in range(1,6))
        say('30 到达叶子，停止。每个父节点又 ≥ 孩子')
        self.play(*[m.animate.set_stroke(GREEN) for i in range(6) for m in (nodes[i],cells[i])],edges[5].animate.set_color(EDGE),run_time=.6)
        self.wait(2)
