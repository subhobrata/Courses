from manim import *

class EulersFormula(Scene):
    """
    A 3Blue1Brown-style visualization of Euler's Formula
    e^(iπ) + 1 = 0
    """

    def construct(self):
        # 3Blue1Brown color scheme
        BLUE_3B1B = "#58C4DD"
        YELLOW_3B1B = "#FC6255"
        GREEN_3B1B = "#83C167"

        # Title sequence (0-4s)
        title = Text("Euler's Formula", font_size=72, color=BLUE_3B1B)
        subtitle = Text("The Most Beautiful Equation", font_size=36, color=GRAY)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP*0.5))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # The formula (4-10s)
        formula = MathTex(
            r"e^{i\pi} + 1 = 0",
            font_size=84,
            color=YELLOW_3B1B
        )
        self.play(Write(formula), run_time=2)
        self.wait(4)

        # Move formula to top (10-11s)
        self.play(
            formula.animate.scale(0.6).to_edge(UP),
            run_time=1
        )

        # Complex plane setup (11-16s)
        plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        ).scale(2)

        plane_labels = plane.add_coordinates()

        real_label = Text("Real", font_size=24).next_to(plane, RIGHT)
        imag_label = Text("Imaginary", font_size=24).next_to(plane, UP)

        self.play(Create(plane), Write(plane_labels), run_time=2)
        self.play(Write(real_label), Write(imag_label))
        self.wait(2)

        # Unit circle (16-20s)
        circle = Circle(radius=2, color=BLUE_3B1B, stroke_width=4)

        self.play(Create(circle), run_time=1.5)
        self.wait(2.5)

        # Euler's formula visualization (20-30s)
        # Point at e^(i*0) = 1
        dot_start = Dot(plane.n2p(1), color=GREEN_3B1B, radius=0.15)
        start_label = MathTex("e^{i \cdot 0} = 1", font_size=30).next_to(dot_start, RIGHT)

        self.play(FadeIn(dot_start), Write(start_label))
        self.wait(1)

        # Animate around the circle to π
        angle_tracker = ValueTracker(0)

        def get_point():
            theta = angle_tracker.get_value()
            return plane.n2p(np.exp(1j * theta))

        dot = Dot(color=GREEN_3B1B, radius=0.15)
        dot.add_updater(lambda m: m.move_to(get_point()))

        # Path trace
        path = TracedPath(dot.get_center, stroke_color=YELLOW_3B1B, stroke_width=4)

        self.add(dot, path)
        self.play(
            angle_tracker.animate.set_value(PI),
            run_time=4,
            rate_func=linear
        )

        # Point at e^(iπ) = -1
        end_label = MathTex("e^{i\pi} = -1", font_size=36, color=YELLOW_3B1B)
        end_label.next_to(dot, LEFT)

        self.play(
            FadeOut(start_label),
            Write(end_label)
        )
        self.wait(2)

        # Highlight the magic (30-35s)
        magic_eq = MathTex(
            "e^{i\pi}", "=", "-1",
            font_size=60,
            color=YELLOW_3B1B
        )
        magic_eq2 = MathTex(
            "e^{i\pi}", "+", "1", "=", "0",
            font_size=60,
            color=YELLOW_3B1B
        )

        magic_eq.to_edge(DOWN)
        magic_eq2.to_edge(DOWN)

        self.play(
            FadeOut(plane_labels),
            FadeOut(real_label),
            FadeOut(imag_label),
            FadeOut(end_label),
            Write(magic_eq)
        )
        self.wait(1)

        self.play(TransformMatchingTex(magic_eq, magic_eq2))
        self.wait(2)

        # Final emphasis (35-40s)
        final_formula = MathTex(
            r"e^{i\pi} + 1 = 0",
            font_size=96,
            color=YELLOW_3B1B
        )

        self.play(
            FadeOut(plane),
            FadeOut(circle),
            FadeOut(dot),
            FadeOut(path),
            FadeOut(formula),
            FadeOut(magic_eq2)
        )

        self.play(Write(final_formula), run_time=2)
        self.wait(3)

        # Fade out
        self.play(FadeOut(final_formula))
        self.wait(1)


class EulersFormulaExplanation(Scene):
    """
    Alternative scene with more detailed explanation
    """

    def construct(self):
        # This is a longer version with more detailed explanation
        title = Text("Understanding e^(iθ)", font_size=60)
        self.play(Write(title))
        self.wait(2)

        # General formula
        general = MathTex(r"e^{i\theta} = \cos(\theta) + i\sin(\theta)")
        general.next_to(title, DOWN, buff=1)
        self.play(Write(general))
        self.wait(3)

        # Special case
        special = MathTex(r"e^{i\pi} = \cos(\pi) + i\sin(\pi)")
        special.next_to(general, DOWN, buff=0.5)
        self.play(Write(special))
        self.wait(2)

        # Evaluate
        evaluate = MathTex(r"e^{i\pi} = -1 + i(0)")
        evaluate.next_to(special, DOWN, buff=0.5)
        self.play(Write(evaluate))
        self.wait(2)

        # Simplify
        simplify = MathTex(r"e^{i\pi} = -1")
        simplify.next_to(evaluate, DOWN, buff=0.5)
        self.play(Write(simplify))
        self.wait(2)

        # Final form
        final = MathTex(r"e^{i\pi} + 1 = 0", color=YELLOW)
        final.scale(1.5)
        self.play(
            FadeOut(title),
            FadeOut(general),
            FadeOut(special),
            FadeOut(evaluate),
            FadeOut(simplify),
            final.animate.move_to(ORIGIN)
        )
        self.wait(3)
