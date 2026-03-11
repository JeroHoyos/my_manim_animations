from manim import *

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8.0

BG_COLOR = "#0B1120"
TEXT_COLOR = "#F8FAFC"
CYAN_HL = "#00E5FF"
BLUE_IN = "#3B82F6"
BLUE_OUT = "#8B5CF6"
LINE_COLOR = "#334155"
HIGHLIGHT = "#FDE047"

class RedNeuronal(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        SAFE_WIDTH = config.frame_width - 1.5 

        grid = NumberPlane(
            x_range=[-10, 10, 1], y_range=[-10, 10, 1],
            background_line_style={"stroke_color": LINE_COLOR, "stroke_width": 1, "stroke_opacity": 0.1},
            axis_config={"stroke_opacity": 0} 
        )
        self.add(grid)

        def cambiar_subtitulo(texto_nuevo):
            lineas = texto_nuevo.split('\n')
            nuevo_sub = VGroup(*[Text(linea, font_size=28, color=TEXT_COLOR) for linea in lineas])
            nuevo_sub.arrange(DOWN, buff=0.15)
            
            if nuevo_sub.width > SAFE_WIDTH:
                nuevo_sub.width = SAFE_WIDTH

            nuevo_sub.to_edge(DOWN, buff=2.2) 
            fondo = BackgroundRectangle(nuevo_sub, color=BG_COLOR, fill_opacity=0.85, buff=0.3)
            return VGroup(fondo, nuevo_sub)

        titulo = VGroup(
            Text("¿Cómo funciona una", weight=BOLD, color=TEXT_COLOR, font_size=36),
            Text("Red Neuronal?", weight=BOLD, color=CYAN_HL, font_size=36)
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=1.8)

        linea_titulo = Line(LEFT * 2.5, RIGHT * 2.5, color=BLUE_IN, stroke_width=3).next_to(titulo, DOWN, buff=0.3)
        
        self.play(Write(titulo), run_time=1.2)
        self.play(GrowFromCenter(linea_titulo), run_time=0.5)

        r = 0.22
        capa_in = VGroup(*[Circle(radius=r, fill_color=BLUE_IN, fill_opacity=1, stroke_color=WHITE, stroke_width=1) for _ in range(3)]).arrange(DOWN, buff=0.4)
        
        capa_in.move_to(LEFT * 1.8 + UP * 0.5)
        
        self.play(FadeIn(capa_in, shift=RIGHT, scale=0.5), run_time=1)
        self.wait(1) 

        sub1 = cambiar_subtitulo("Imagina una maquina de datos.\nEntra información, y sale una predicción.")
        self.play(FadeIn(sub1, shift=UP*0.5), run_time=0.8)

        hid_1 = VGroup(*[Circle(radius=r, fill_color=CYAN_HL, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1) for _ in range(5)]).arrange(DOWN, buff=0.3)
        hid_2 = VGroup(*[Circle(radius=r, fill_color=CYAN_HL, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1) for _ in range(5)]).arrange(DOWN, buff=0.3)
        capa_out = VGroup(*[Circle(radius=r, fill_color=BLUE_OUT, fill_opacity=1, stroke_color=WHITE, stroke_width=1) for _ in range(2)]).arrange(DOWN, buff=0.4)

        red_resto = VGroup(hid_1, hid_2, capa_out).arrange(RIGHT, buff=0.8)
        red_resto.next_to(capa_in, RIGHT, buff=0.8)

        conexiones_in_h1 = VGroup(*[Line(n1.get_right(), n2.get_left(), stroke_width=1.5, color=LINE_COLOR, stroke_opacity=0.5) for n1 in capa_in for n2 in hid_1])
        conexiones_h1_h2 = VGroup(*[Line(n1.get_right(), n2.get_left(), stroke_width=1.5, color=LINE_COLOR, stroke_opacity=0.5) for n1 in hid_1 for n2 in hid_2])
        conexiones_h2_out = VGroup(*[Line(n1.get_right(), n2.get_left(), stroke_width=1.5, color=LINE_COLOR, stroke_opacity=0.5) for n1 in hid_2 for n2 in capa_out])

        self.play(
            LaggedStartMap(Create, conexiones_in_h1, lag_ratio=0.01), FadeIn(hid_1, shift=LEFT*0.2),
            LaggedStartMap(Create, conexiones_h1_h2, lag_ratio=0.01), FadeIn(hid_2, shift=LEFT*0.2),
            LaggedStartMap(Create, conexiones_h2_out, lag_ratio=0.01), FadeIn(capa_out, shift=LEFT*0.2),
            run_time=2.5
        )

        def crear_y_reproducir_flujo(conexiones):
            dots = VGroup(*[
                Dot(radius=0.08, color=HIGHLIGHT, fill_opacity=1).move_to(line.get_start()) 
                for line in conexiones
            ])
            self.play(FadeIn(dots, run_time=0.15))
            self.play(LaggedStart(*[MoveAlongPath(dot, line) for dot, line in zip(dots, conexiones)], lag_ratio=0.05, run_time=1.0))
            self.play(FadeOut(dots, run_time=0.15))

        crear_y_reproducir_flujo(conexiones_in_h1)
        crear_y_reproducir_flujo(conexiones_h1_h2)
        crear_y_reproducir_flujo(conexiones_h2_out)
        
        eq_top = MathTex(r"f(x) = \phi_3(\phi_2(\phi_1(x)))", color=TEXT_COLOR, font_size=32).next_to(red_resto, DOWN, buff=1)
        self.play(Write(eq_top), run_time=1)
        self.wait(1) 

        sub2 = cambiar_subtitulo("Pero hagamos zoom...\n¿Qué pasa dentro de UNA sola neurona?")
        self.play(Transform(sub1, sub2), run_time=0.8)

        neurona_objetivo = hid_1[2]
       
        neurona_gigante = Circle(radius=1.5, fill_color=BG_COLOR, fill_opacity=1, stroke_color=CYAN_HL, stroke_width=4).shift(UP * 0.5)
        
        elementos_a_ocultar = VGroup(capa_in, hid_1[0:2], hid_1[3:], hid_2, capa_out, conexiones_in_h1, conexiones_h1_h2, conexiones_h2_out, eq_top)
        
        self.play(
            FadeOut(elementos_a_ocultar),
            Transform(neurona_objetivo, neurona_gigante),
            run_time=1.5,
            rate_func=smooth
        )

        sumatoria = MathTex(r"\Sigma", color=TEXT_COLOR, font_size=60).move_to(neurona_gigante).shift(LEFT * 0.5)
        separador = Line(neurona_gigante.get_top() + DOWN*0.1, neurona_gigante.get_bottom() + UP*0.1, color=CYAN_HL, stroke_width=2)
        
        ejes_act = Axes(
            x_range=[-2, 2], y_range=[-0.5, 1.5], 
            x_length=1.0, y_length=1.0, 
            tips=False, 
            axis_config={"color": LINE_COLOR, "include_ticks": False}
        ).move_to(neurona_gigante).shift(RIGHT * 0.5)
        
        curva_act = ejes_act.plot(lambda x: x if x > 0 else 0, color=BLUE_OUT, stroke_width=4) 
        grupo_activacion = VGroup(ejes_act, curva_act)

        self.play(Write(sumatoria), Create(separador), FadeIn(grupo_activacion, shift=UP*0.2), run_time=1.5)
        self.wait(1) 

        sub3 = cambiar_subtitulo("1. Recibe datos y multiplica por un 'peso' (W)\npara darle más o menos importancia.")
        self.play(Transform(sub1, sub3), run_time=0.8)

        entradas_x_coords = -3.0 
        entradas_y_buff = 0.6
        
        start_y = 0.5 + (entradas_y_buff * 1.5)

        x1 = MathTex(r"x_1", color=BLUE_IN).move_to([entradas_x_coords, start_y, 0])
        x2 = MathTex(r"x_2", color=BLUE_IN).move_to([entradas_x_coords, start_y - entradas_y_buff, 0])
        dots_x = MathTex(r"\vdots", color=TEXT_COLOR).move_to([entradas_x_coords, start_y - (entradas_y_buff * 2), 0])
        xn = MathTex(r"x_n", color=BLUE_IN).move_to([entradas_x_coords, start_y - (entradas_y_buff * 3), 0])
        
        entradas_text = VGroup(x1, x2, dots_x, xn)

        longitud_flecha = 1.3
        flechas_in = VGroup()
        for e in [x1, x2, xn]:
            arrow = Arrow(
                start=e.get_right(),
                end=e.get_right() + RIGHT * longitud_flecha, 
                buff=0.15, 
                color=LINE_COLOR
            )
            flechas_in.add(arrow)

        pesos_text = VGroup(
            MathTex(r"w_1", color=CYAN_HL).move_to(flechas_in[0].get_center() + UP * 0.35).scale(0.8),
            MathTex(r"w_2", color=CYAN_HL).move_to(flechas_in[1].get_center() + UP * 0.35).scale(0.8),
            MathTex(r"w_n", color=CYAN_HL).move_to(flechas_in[2].get_center() + UP * 0.35).scale(0.8)
        )

        neurona_edge = neurona_gigante.get_left()
        conectores = VGroup(*[
            Line(arrow.get_end(), [neurona_edge[0], arrow.get_end()[1], 0], color=LINE_COLOR, stroke_opacity=0.5)
            for arrow in flechas_in
        ])

        self.play(
            LaggedStart(
                *[AnimationGroup(FadeIn(e, shift=RIGHT), GrowArrow(f)) for e, f in zip([x1, x2, xn], flechas_in)], 
                lag_ratio=0.2
            ),
            FadeIn(dots_x),
            run_time=2
        )
        self.play(FadeIn(pesos_text, shift=DOWN*0.3), Create(conectores), run_time=1)
        self.wait(1) 

        sub4 = cambiar_subtitulo("2. Suma todo y le añade un sesgo (b)\npara ajustar el umbral.")
        self.play(Transform(sub1, sub4), run_time=0.8)

        bias_text = MathTex(r"b", color=HIGHLIGHT).next_to(neurona_gigante, UP, buff=0.6)
        flecha_bias = Arrow(bias_text.get_bottom(), neurona_gigante.get_top(), buff=0.1, color=HIGHLIGHT)

        self.play(FadeIn(bias_text, shift=DOWN), GrowArrow(flecha_bias), run_time=1)
        self.play(Indicate(sumatoria, color=HIGHLIGHT, scale_factor=1.5), run_time=1)
        self.wait(1) 

        sub5 = cambiar_subtitulo("3. Pasa por una función de activación\nque decide si dispara o no.")
        self.play(Transform(sub1, sub5), run_time=0.8)

        flecha_out = Arrow(neurona_gigante.get_right(), neurona_gigante.get_right() + RIGHT * 1.0, color=BLUE_OUT)
        salida_text = MathTex(r"\phi(x)", color=BLUE_OUT).next_to(flecha_out, RIGHT)

        self.play(GrowArrow(flecha_out), run_time=0.5)

        self.play(Create(curva_act), Write(salida_text), run_time=1.5)

        eq_final = MathTex(
            r"\phi(x)", r" = ", r"\sigma", r"\left(", r"\sum ", r"x_i", r" w_i", r" + ", r"b", r"\right)",
            color=TEXT_COLOR, font_size=34 
        ).next_to(neurona_gigante, DOWN, buff=1.0)
     
        if eq_final.width > SAFE_WIDTH:
            eq_final.width = SAFE_WIDTH

        eq_final[0].set_color(BLUE_OUT)  
        eq_final[2].set_color(BLUE_OUT)  
        eq_final[5].set_color(BLUE_IN)   
        eq_final[6].set_color(CYAN_HL)   
        eq_final[8].set_color(HIGHLIGHT)   

        self.play(
            TransformFromCopy(salida_text, eq_final[0]),
            Write(eq_final[1]), Write(eq_final[2]), Write(eq_final[3]),
            TransformFromCopy(sumatoria, eq_final[4]),
            TransformFromCopy(x2, eq_final[5]),
            TransformFromCopy(pesos_text[1], eq_final[6]),
            Write(eq_final[7]),
            TransformFromCopy(bias_text, eq_final[8]),
            Write(eq_final[9]),
            run_time=2.5
        )
        self.wait(1.5) 

        sub6 = cambiar_subtitulo("¡Y ya está! Miles de estas trabajando juntas\nes lo que llamamos Deep Learning.")
        self.play(Transform(sub1, sub6), run_time=1)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)