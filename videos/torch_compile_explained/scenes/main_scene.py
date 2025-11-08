from manim import *
import numpy as np

# 3Blue1Brown color scheme
BLUE_3B1B = "#58C4DD"
YELLOW_3B1B = "#FC6255"
GREEN_3B1B = "#83C167"
PURPLE_3B1B = "#9A72AC"
ORANGE_3B1B = "#FF8C00"

class TorchCompileExplained(Scene):
    """
    Complete torch.compile explanation video
    ~5 minutes with synchronized narration
    """

    def construct(self):
        # Introduction (0-15s)
        self.intro_section()

        # Section 1: What is torch.compile (15-45s)
        self.what_is_compile_section()

        # Section 2: Compilation Pipeline (45-90s)
        self.pipeline_section()

        # Section 3: API Parameters (90-150s)
        self.api_section()

        # Section 4: Code Examples (150-195s)
        self.code_examples_section()

        # Section 5: Dynamic Shapes (195-225s)
        self.dynamic_shapes_section()

        # Section 6: Graph Breaks (225-260s)
        self.graph_breaks_section()

        # Section 7: Performance (260-285s)
        self.performance_section()

        # Conclusion (285-300s)
        self.conclusion_section()

    def intro_section(self):
        """Introduction (0-15s)"""
        # Title
        title = Text("torch.compile", font_size=84, color=BLUE_3B1B, weight=BOLD)
        subtitle = Text("A Complete Guide", font_size=42, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP*0.3))
        self.wait(1)

        # PyTorch 2.x badge
        badge = Text("PyTorch 2.x", font_size=32, color=YELLOW_3B1B)
        badge.to_edge(UR, buff=0.5)
        self.play(FadeIn(badge, scale=0.5))
        self.wait(1.5)

        # Clear
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            badge.animate.scale(0.5).to_corner(UR, buff=0.3)
        )
        self.wait(0.5)

    def what_is_compile_section(self):
        """What is torch.compile? (15-45s)"""
        # Show the transformation
        before = Code(
            code="model = MyModel()\noutput = model(input)",
            language="python",
            font_size=28,
            background="window"
        ).scale(0.7)
        before.to_edge(LEFT, buff=1)

        after = Code(
            code="model = MyModel()\nmodel = torch.compile(model)\noutput = model(input)",
            language="python",
            font_size=28,
            background="window"
        ).scale(0.7)
        after.to_edge(RIGHT, buff=1)

        arrow = Arrow(before.get_right(), after.get_left(), color=GREEN_3B1B, buff=0.3)
        speedup = Text("2-3x faster!", font_size=32, color=YELLOW_3B1B)
        speedup.next_to(arrow, UP)

        self.play(FadeIn(before), run_time=1)
        self.wait(2)
        self.play(
            GrowArrow(arrow),
            Write(speedup)
        )
        self.wait(1)
        self.play(FadeIn(after), run_time=1)
        self.wait(3)

        # Show the compilation concept
        self.play(
            FadeOut(before),
            FadeOut(after),
            FadeOut(arrow),
            FadeOut(speedup)
        )

        # Pipeline preview
        boxes = VGroup(
            *[Rectangle(width=2.5, height=1, color=BLUE_3B1B, fill_opacity=0.2)
              for _ in range(4)]
        ).arrange(RIGHT, buff=0.5)

        labels = VGroup(
            Text("TorchDynamo", font_size=20),
            Text("AOTAutograd", font_size=20),
            Text("Lowering", font_size=20),
            Text("TorchInductor", font_size=20)
        )

        for box, label in zip(boxes, labels):
            label.move_to(box)

        arrows = VGroup(*[
            Arrow(boxes[i].get_right(), boxes[i+1].get_left(), buff=0.1, color=GREEN_3B1B)
            for i in range(3)
        ])

        pipeline = VGroup(boxes, labels, arrows)
        pipeline.scale(0.8)

        self.play(
            LaggedStart(*[FadeIn(box) for box in boxes], lag_ratio=0.2),
            run_time=2
        )
        self.play(
            LaggedStart(*[Write(label) for label in labels], lag_ratio=0.2),
            run_time=2
        )
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.3),
            run_time=1.5
        )
        self.wait(3)

        self.play(FadeOut(pipeline))
        self.wait(0.5)

    def pipeline_section(self):
        """Compilation Pipeline (45-90s)"""
        # Stage 1: TorchDynamo (10s)
        self.show_dynamo_stage()

        # Stage 2: AOTAutograd (8s)
        self.show_aot_stage()

        # Stage 3: Lowering (7s)
        self.show_lowering_stage()

        # Stage 4: TorchInductor (10s)
        self.show_inductor_stage()

        self.wait(1)

    def show_dynamo_stage(self):
        """TorchDynamo visualization"""
        title = Text("Stage 1: TorchDynamo", font_size=48, color=BLUE_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=0.8)
        self.wait(0.5)

        # Python bytecode to graph
        python_code = Code(
            code="def forward(x):\n    x = x + 1\n    x = x * 2\n    return x",
            language="python",
            font_size=24,
            background="window"
        ).scale(0.6).to_edge(LEFT, buff=1)

        # Graph representation
        graph = VGroup()
        nodes = VGroup(
            *[Circle(radius=0.3, color=GREEN_3B1B, fill_opacity=0.3) for _ in range(3)]
        ).arrange(DOWN, buff=0.5)

        node_labels = VGroup(
            Text("add", font_size=18),
            Text("mul", font_size=18),
            Text("return", font_size=18)
        )

        for node, label in zip(nodes, node_labels):
            label.move_to(node)

        edges = VGroup(
            Arrow(nodes[0].get_bottom(), nodes[1].get_top(), buff=0.1, color=BLUE_3B1B),
            Arrow(nodes[1].get_bottom(), nodes[2].get_top(), buff=0.1, color=BLUE_3B1B)
        )

        graph.add(nodes, node_labels, edges)
        graph.scale(0.8).to_edge(RIGHT, buff=1)

        transform_arrow = Arrow(
            python_code.get_right(),
            graph.get_left(),
            color=YELLOW_3B1B,
            buff=0.3
        )

        self.play(FadeIn(python_code), run_time=1)
        self.wait(1)
        self.play(GrowArrow(transform_arrow))
        self.wait(0.5)
        self.play(
            LaggedStart(
                *[FadeIn(node) for node in nodes],
                *[Write(label) for label in node_labels],
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.play(
            LaggedStart(*[GrowArrow(edge) for edge in edges], lag_ratio=0.4),
            run_time=1
        )
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(python_code),
            FadeOut(transform_arrow),
            FadeOut(graph)
        )

    def show_aot_stage(self):
        """AOTAutograd visualization"""
        title = Text("Stage 2: AOTAutograd", font_size=48, color=GREEN_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=0.8)
        self.wait(0.5)

        # Forward and backward graphs
        forward_box = Rectangle(width=3, height=2, color=BLUE_3B1B, fill_opacity=0.2)
        forward_label = Text("Forward\nGraph", font_size=28)
        forward_label.move_to(forward_box)
        forward = VGroup(forward_box, forward_label).shift(LEFT*2.5)

        backward_box = Rectangle(width=3, height=2, color=YELLOW_3B1B, fill_opacity=0.2)
        backward_label = Text("Backward\nGraph", font_size=28)
        backward_label.move_to(backward_box)
        backward = VGroup(backward_box, backward_label).shift(RIGHT*2.5)

        arrow = DoubleArrow(
            forward.get_right(),
            backward.get_left(),
            color=GREEN_3B1B,
            buff=0.3
        )

        self.play(FadeIn(forward), run_time=1)
        self.wait(1)
        self.play(GrowArrow(arrow))
        self.wait(0.5)
        self.play(FadeIn(backward), run_time=1)

        # Add "Autograd" label
        autograd_label = Text("Autograd Magic ✨", font_size=24, color=GREEN_3B1B)
        autograd_label.next_to(arrow, UP)
        self.play(Write(autograd_label))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(forward),
            FadeOut(backward),
            FadeOut(arrow),
            FadeOut(autograd_label)
        )

    def show_lowering_stage(self):
        """Lowering visualization"""
        title = Text("Stage 3: Lowering", font_size=48, color=PURPLE_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=0.8)
        self.wait(0.5)

        # Many ops to core ops
        many_ops = VGroup(
            *[Text(op, font_size=20) for op in
              ["Conv2d", "BatchNorm", "ReLU", "MaxPool", "Linear", "..."]]
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        many_ops.to_edge(LEFT, buff=1.5)

        core_ops = VGroup(
            *[Text(op, font_size=20, color=GREEN_3B1B) for op in
              ["aten::add", "aten::mul", "aten::conv", "prims::*"]]
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        core_ops.to_edge(RIGHT, buff=1.5)

        arrow = Arrow(many_ops.get_right(), core_ops.get_left(), color=BLUE_3B1B, buff=0.5)
        reduction_label = Text("Canonical Ops", font_size=24, color=YELLOW_3B1B)
        reduction_label.next_to(arrow, UP)

        self.play(
            LaggedStart(*[FadeIn(op, shift=RIGHT*0.2) for op in many_ops], lag_ratio=0.15),
            run_time=2
        )
        self.wait(0.5)
        self.play(GrowArrow(arrow), Write(reduction_label))
        self.wait(0.5)
        self.play(
            LaggedStart(*[FadeIn(op, shift=LEFT*0.2) for op in core_ops], lag_ratio=0.2),
            run_time=1.5
        )
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(many_ops),
            FadeOut(core_ops),
            FadeOut(arrow),
            FadeOut(reduction_label)
        )

    def show_inductor_stage(self):
        """TorchInductor visualization"""
        title = Text("Stage 4: TorchInductor", font_size=48, color=ORANGE_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=0.8)
        self.wait(0.5)

        # Graph to kernels
        graph_box = Rectangle(width=2.5, height=2.5, color=BLUE_3B1B, fill_opacity=0.2)
        graph_label = Text("Optimized\nGraph", font_size=24)
        graph_label.move_to(graph_box)
        graph = VGroup(graph_box, graph_label).shift(LEFT*3)

        # GPU and CPU kernels
        gpu_kernel = Rectangle(width=2.2, height=1, color=GREEN_3B1B, fill_opacity=0.2)
        gpu_label = Text("Triton\nKernel", font_size=20)
        gpu_label.move_to(gpu_kernel)
        gpu = VGroup(gpu_kernel, gpu_label).shift(RIGHT*2.5 + UP*1)

        cpu_kernel = Rectangle(width=2.2, height=1, color=PURPLE_3B1B, fill_opacity=0.2)
        cpu_label = Text("C++/OpenMP\nKernel", font_size=20)
        cpu_label.move_to(cpu_kernel)
        cpu = VGroup(cpu_kernel, cpu_label).shift(RIGHT*2.5 + DOWN*1)

        arrow_gpu = Arrow(graph.get_right(), gpu.get_left(), color=GREEN_3B1B, buff=0.2)
        arrow_cpu = Arrow(graph.get_right(), cpu.get_left(), color=PURPLE_3B1B, buff=0.2)

        self.play(FadeIn(graph), run_time=1)
        self.wait(1)
        self.play(GrowArrow(arrow_gpu))
        self.play(FadeIn(gpu, shift=LEFT*0.3))
        self.wait(0.5)
        self.play(GrowArrow(arrow_cpu))
        self.play(FadeIn(cpu, shift=LEFT*0.3))
        self.wait(2)

        # Add optimization labels
        fusion = Text("Fusion", font_size=18, color=YELLOW_3B1B)
        fusion.next_to(graph, DOWN, buff=0.3)
        self.play(FadeIn(fusion, scale=0.5))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(graph),
            FadeOut(gpu),
            FadeOut(cpu),
            FadeOut(arrow_gpu),
            FadeOut(arrow_cpu),
            FadeOut(fusion)
        )

    def api_section(self):
        """API Parameters (90-150s)"""
        title = Text("Key Parameters", font_size=54, color=BLUE_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=1)
        self.wait(1)

        # Show parameters one by one
        params = [
            ("fullgraph", "True/False", "Require single graph?", 15),
            ("dynamic", "True/False/None", "Handle dynamic shapes?", 12),
            ("mode", "default/reduce-overhead/max-autotune", "Performance preset", 15),
            ("backend", "inductor/eager/aot_eager", "Compiler backend", 10)
        ]

        y_start = 2
        param_objects = []

        for i, (name, values, desc, duration) in enumerate(params):
            param_group = self.create_parameter_display(name, values, desc)
            param_group.shift(UP*(y_start - i*1.3))
            param_objects.append(param_group)

            self.play(FadeIn(param_group, shift=UP*0.3), run_time=0.8)
            self.wait(duration / 10)  # Scaled wait time

        self.wait(2)

        self.play(
            FadeOut(title),
            *[FadeOut(obj) for obj in param_objects]
        )

    def create_parameter_display(self, name, values, description):
        """Helper to create parameter display"""
        param_name = Text(name, font_size=32, color=YELLOW_3B1B, weight=BOLD)
        param_values = Text(values, font_size=20, color=GREEN_3B1B)
        param_desc = Text(description, font_size=18, color=GRAY)

        param_values.next_to(param_name, RIGHT, buff=0.5)
        param_desc.next_to(param_name, DOWN, buff=0.2, aligned_edge=LEFT)

        return VGroup(param_name, param_values, param_desc)

    def code_examples_section(self):
        """Code Examples (150-195s)"""
        # Example 1: Inference
        title1 = Text("Example: Inference", font_size=42, color=BLUE_3B1B)
        title1.to_edge(UP)

        code1 = Code(
            code="""model = MLP(1024).cuda()
model = torch.compile(model)

x = torch.randn(32, 1024).cuda()
y = model(x)  # First call compiles""",
            language="python",
            font_size=22,
            background="window",
            insert_line_no=False
        ).scale(0.75)

        self.play(Write(title1), run_time=0.8)
        self.wait(1)
        self.play(FadeIn(code1), run_time=1.5)
        self.wait(8)

        self.play(FadeOut(title1), FadeOut(code1))
        self.wait(0.5)

        # Example 2: Training
        title2 = Text("Example: Training", font_size=42, color=GREEN_3B1B)
        title2.to_edge(UP)

        code2 = Code(
            code="""model = torch.compile(model).cuda()
optimizer = torch.optim.AdamW(model.parameters())

for x, y in loader:
    optimizer.zero_grad()
    loss = F.mse_loss(model(x), y)
    loss.backward()  # AOTAutograd!
    optimizer.step()""",
            language="python",
            font_size=20,
            background="window",
            insert_line_no=False
        ).scale(0.75)

        self.play(Write(title2), run_time=0.8)
        self.wait(1)
        self.play(FadeIn(code2), run_time=1.5)
        self.wait(10)

        self.play(FadeOut(title2), FadeOut(code2))
        self.wait(0.5)

        # Example 3: DDP
        title3 = Text("Example: DDP (Important Order!)", font_size=42, color=PURPLE_3B1B)
        title3.to_edge(UP)

        code3 = Code(
            code="""# Correct order:
model = model.to(device)        # 1️⃣ Device
model = DDP(model)              # 2️⃣ DDP wrap
model = torch.compile(model)    # 3️⃣ Compile""",
            language="python",
            font_size=24,
            background="window",
            insert_line_no=False
        ).scale(0.8)

        self.play(Write(title3), run_time=1)
        self.wait(1)
        self.play(FadeIn(code3), run_time=1.5)
        self.wait(8)

        self.play(FadeOut(title3), FadeOut(code3))

    def dynamic_shapes_section(self):
        """Dynamic Shapes (195-225s)"""
        title = Text("Dynamic Shapes", font_size=54, color=ORANGE_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=1)
        self.wait(1)

        # Show shape variations
        shapes = VGroup()
        for i, size in enumerate([32, 64, 128]):
            rect = Rectangle(
                width=size/30,
                height=1,
                color=BLUE_3B1B,
                fill_opacity=0.3
            )
            label = Text(f"{size}", font_size=20)
            label.next_to(rect, DOWN)
            shape_group = VGroup(rect, label)
            shape_group.shift(LEFT*3 + DOWN*i*1.2)
            shapes.add(shape_group)

        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT*0.3) for s in shapes], lag_ratio=0.3),
            run_time=2
        )
        self.wait(2)

        # Show dynamic vs static
        dynamic_label = Text("dynamic=True", font_size=28, color=GREEN_3B1B)
        dynamic_label.shift(RIGHT*2 + UP*1)
        dynamic_desc = Text("One kernel\nfor all sizes", font_size=20, color=GRAY)
        dynamic_desc.next_to(dynamic_label, DOWN)

        static_label = Text("dynamic=False", font_size=28, color=YELLOW_3B1B)
        static_label.shift(RIGHT*2 + DOWN*1.5)
        static_desc = Text("Specialized kernels\nper size", font_size=20, color=GRAY)
        static_desc.next_to(static_label, DOWN)

        self.play(
            Write(dynamic_label),
            FadeIn(dynamic_desc, shift=UP*0.2)
        )
        self.wait(3)

        self.play(
            Write(static_label),
            FadeIn(static_desc, shift=UP*0.2)
        )
        self.wait(5)

        # Trade-off visualization
        tradeoff = Text("Trade-off: Flexibility vs Speed", font_size=24, color=YELLOW_3B1B)
        tradeoff.to_edge(DOWN, buff=1)
        self.play(Write(tradeoff))
        self.wait(4)

        self.play(
            FadeOut(title),
            FadeOut(shapes),
            FadeOut(dynamic_label),
            FadeOut(dynamic_desc),
            FadeOut(static_label),
            FadeOut(static_desc),
            FadeOut(tradeoff)
        )

    def graph_breaks_section(self):
        """Graph Breaks (225-260s)"""
        title = Text("Graph Breaks", font_size=54, color=YELLOW_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=1)
        self.wait(1)

        # Show problematic code
        bad_code = Code(
            code="""def forward(x):
    x = x + 1
    print(x.shape)      # ❌ Graph break!
    if x.item() > 0:    # ❌ Graph break!
        x = x * 2
    return x""",
            language="python",
            font_size=22,
            background="window",
            insert_line_no=False
        ).scale(0.7).to_edge(LEFT, buff=1)

        # Show graph representation with breaks
        graph_parts = VGroup()

        # Part 1
        part1 = Rectangle(width=1.5, height=0.8, color=GREEN_3B1B, fill_opacity=0.3)
        part1_label = Text("Graph 1", font_size=16)
        part1_label.move_to(part1)

        # Break
        break1 = Text("BREAK", font_size=14, color=RED, weight=BOLD)

        # Part 2
        part2 = Rectangle(width=1.5, height=0.8, color=GREEN_3B1B, fill_opacity=0.3)
        part2_label = Text("Graph 2", font_size=16)
        part2_label.move_to(part2)

        # Break
        break2 = Text("BREAK", font_size=14, color=RED, weight=BOLD)

        # Part 3
        part3 = Rectangle(width=1.5, height=0.8, color=GREEN_3B1B, fill_opacity=0.3)
        part3_label = Text("Graph 3", font_size=16)
        part3_label.move_to(part3)

        graph_parts = VGroup(
            VGroup(part1, part1_label),
            break1,
            VGroup(part2, part2_label),
            break2,
            VGroup(part3, part3_label)
        ).arrange(DOWN, buff=0.3)
        graph_parts.to_edge(RIGHT, buff=1)

        self.play(FadeIn(bad_code), run_time=1.5)
        self.wait(3)

        self.play(
            LaggedStart(*[FadeIn(part, shift=LEFT*0.2) for part in graph_parts], lag_ratio=0.3),
            run_time=3
        )
        self.wait(3)

        self.play(FadeOut(bad_code), FadeOut(graph_parts))
        self.wait(0.5)

        # Show solutions
        solutions_title = Text("Solutions", font_size=42, color=GREEN_3B1B)
        solutions_title.to_edge(UP, buff=1.5)

        solutions = VGroup(
            Text("✓ Use torch._dynamo.explain()", font_size=24),
            Text("✓ Set fullgraph=True to catch breaks", font_size=24),
            Text("✓ Avoid .item() in control flow", font_size=24),
            Text("✓ Use torch.where instead of if/else", font_size=24),
            Text("✓ Mark functions with @torch.compiler.disable", font_size=24)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        solutions.next_to(solutions_title, DOWN, buff=0.5)

        self.play(Write(solutions_title), run_time=0.8)
        self.wait(1)
        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT*0.2) for s in solutions], lag_ratio=0.4),
            run_time=4
        )
        self.wait(8)

        self.play(
            FadeOut(title),
            FadeOut(solutions_title),
            FadeOut(solutions)
        )

    def performance_section(self):
        """Performance Tips (260-285s)"""
        title = Text("Performance Playbook", font_size=54, color=GREEN_3B1B)
        title.to_edge(UP)

        self.play(Write(title), run_time=1)
        self.wait(1)

        # Show performance ladder
        tips = [
            ("1. Start simple", "torch.compile(model)", BLUE_3B1B),
            ("2. Small batches?", "mode='reduce-overhead'", GREEN_3B1B),
            ("3. Max performance?", "mode='max-autotune'", ORANGE_3B1B),
            ("4. Fix graph breaks", "Use debugging tools", YELLOW_3B1B),
            ("5. Keep shapes steady", "Avoid dynamic when possible", PURPLE_3B1B)
        ]

        y_pos = 2
        tip_objects = []

        for i, (step, detail, color) in enumerate(tips):
            step_text = Text(step, font_size=28, color=color, weight=BOLD)
            detail_text = Text(detail, font_size=20, color=GRAY)
            detail_text.next_to(step_text, RIGHT, buff=0.5)

            tip_group = VGroup(step_text, detail_text)
            tip_group.shift(UP*(y_pos - i*0.9))
            tip_objects.append(tip_group)

            self.play(FadeIn(tip_group, shift=UP*0.2), run_time=0.6)
            self.wait(3.5)

        self.wait(3)

        self.play(
            FadeOut(title),
            *[FadeOut(obj) for obj in tip_objects]
        )

    def conclusion_section(self):
        """Conclusion (285-300s)"""
        # Summary points
        summary = VGroup(
            Text("✓ torch.compile speeds up PyTorch code", font_size=28, color=GREEN_3B1B),
            Text("✓ 4-stage pipeline: Dynamo → AOT → Lower → Inductor", font_size=28, color=BLUE_3B1B),
            Text("✓ Use modes and options to tune performance", font_size=28, color=ORANGE_3B1B),
            Text("✓ Debug graph breaks with explain()", font_size=28, color=YELLOW_3B1B),
            Text("✓ Profile and iterate!", font_size=28, color=PURPLE_3B1B)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            LaggedStart(*[FadeIn(s, shift=UP*0.3) for s in summary], lag_ratio=0.4),
            run_time=4
        )
        self.wait(5)

        # Final message
        self.play(FadeOut(summary))
        self.wait(0.5)

        final = Text("Happy Compiling! 🚀", font_size=64, color=BLUE_3B1B, weight=BOLD)
        self.play(Write(final), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(final))
        self.wait(0.5)
