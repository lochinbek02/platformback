from manim import *

class MyScene(Scene):
    def construct(self):
        square = Square()  # To'rtburchak chizish
        self.play(Create(square))  # To'rtburchakni chizish
        self.wait(1)  # 1 soniya kutish
