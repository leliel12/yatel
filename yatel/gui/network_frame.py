import pilas

motor = pilas._crear_motor("qt")

pilas.mundo = pilas.Mundo(motor, ancho=800, alto=600, titulo="test")

pilas.ejecutar()
