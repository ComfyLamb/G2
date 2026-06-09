#módulos
import os
import random
import pygame

#estados
ESTADO_INICIO = "inicio"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_JUGANDO = "jugando"
ESTADO_DERROTA = "derrota"
ESTADO_VICTORIA = "victoria"

DIR_PANTALLAS = os.path.join(os.path.dirname(__file__), "data", "pantallas")

PANTALLA_INICIO = "pantalla_inicio.bmp"
PANTALLA_INSTRUCCIONES = "pantalla_instrucciones.bmp"
PANTALLA_VICTORIA = "pantalla_victoria.bmp"
PANTALLA_DERROTA = "pantalla_derrota.bmp"

#delays de movimiento
RETRASO = 200
RETRASO2 = 100

#códigos de elementos
VACIO = 0
OBSTACULO = 1
JUGADOR = 2
DIAMANTE = 3
TOPO = 4

#niveles
NIVELES = [
    {
        "diamantes": 5, "rocas": 25},
        {"diamantes": 5, "rocas": 30},
        {"diamantes": 5, "rocas":35
    }    
]

#tablero
FILAS = 15
COLUMNAS = 15


def aparecer_aleatorio(tablero, id_elem):
    """
    Coloca un elemento en una casilla vacía aleatoria del tablero.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - id_elem: El número identificador del elemento que queremos colocar.

    Retorna:
        - (columna, fila): Tupla que indica posición en la que se colocó el elemento.
    """

    # Debemos detectar los espacios vacíos, para ello recorremos
    # el tablero y almacenamos tuplas de (columna, fila) las posiciones
    # en las que un elemento "VACIO" (el número 0 en este caso) se encuentre.
    vacios = []

    # Forma vista en clases de recorrer el arreglo multidimensional.
    # Tanto fila como columna son números.
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            # Obtenemos el elemento que se encuentra en esa fila y columna.
            elem_pos = tablero[fila][columna]

            if elem_pos == VACIO:
                # Al utilizar los paréntesis () dentro de la función, lo estaremos
                # añadiendo como una tupla con la estructura (columna, fila).
                vacios.append((columna, fila))

    # También se puede utilizar comprensión de listas para rellenar el arreglo
    # a la vez que lo recorremos:
    #
    # vacios = [
    #     (columna, fila)
    #     for fila in range(FILAS)
    #     for columna in range(COLUMNAS)
    #     if tablero[fila][columna] == VACIO
    # ]

    # Si no hay casillas vacías, retornamos un valor especial.
    if len(vacios) == 0:
        return -1, -1

    # Usando la función random.choice(lista) podremos obtener una tupla
    # aleatoria desde el arreglo "vacios" que definimos anteriormente.
    columna, fila = random.choice(vacios)

    # Finalmente, colocamos el elemento al poner su número en la casilla
    # del tablero correspondiente.
    tablero[fila][columna] = id_elem

    return columna, fila


def poblar_tablero(tablero, nivel):
    print("Cargando nivel:", nivel + 1)
    config = NIVELES[nivel]

    for i in range(config["rocas"]):
        aparecer_aleatorio(tablero, OBSTACULO)

    for i in range(config["diamantes"]):
        aparecer_aleatorio(tablero, DIAMANTE)


def refrescar_tablero(screen, tablero, diamantes, objetivo, fuente):

    screen.fill("gray30")

    alto_elem = screen.get_height() / FILAS
    ancho_elem = screen.get_width() / COLUMNAS

    radio = ancho_elem / 2

    pos_y = 0

    for i in range(FILAS):
        # Posición en eje "x" en unidad de píxeles.
        pos_x = 0
        for j in range(COLUMNAS):
            if tablero[i][j] == OBSTACULO:
                # Dibuja un rectángulo en la posición (pos_x, pos_y) y que sea
                # de tamaño (ancho_elem, alto_elem) y color negro.
                pygame.draw.rect(
                    screen,
                    "grey",
                    pygame.Rect((pos_x, pos_y), (ancho_elem, alto_elem)),
                )
            elif tablero[i][j] == JUGADOR:
                # Dibujamos un círculo verde en la posición (pos_x + radio, pos_y + radio),
                # con un radio definido por la variable "radio" (ancho_elem / 2).
                pygame.draw.circle(
                    screen,
                    "yellow",
                    (pos_x + radio, pos_y + radio),
                    radio,
                )
            elif tablero[i][j] == DIAMANTE:

                pygame.draw.polygon(
                screen,
                "cyan",
                [
                    (pos_x + ancho_elem // 2, pos_y + 5),                  # arriba
                    (pos_x + ancho_elem - 5, pos_y + alto_elem // 2),      # derecha
                    (pos_x + ancho_elem // 2, pos_y + alto_elem - 5),      # abajo
                    (pos_x + 5, pos_y + alto_elem // 2)                    # izquierda
                ]
                )   

            pos_x += ancho_elem
        pos_y += alto_elem
    
    texto = fuente.render(
        f"Diamantes: {diamantes}/{objetivo}",
        True,
        (255, 255, 255)
    )

    screen.blit(texto, (10, 10))
    pygame.display.flip()


def cambiar_direccion(keys, direccion_actual):
    """
    Cambia la dirección del jugador.

    Parámetros:
        - keys: Arreglo de teclas presionadas.
        - direccion_actual: La dirección en la que estaba avanzando justo antes de analizar
            si hubo un cambio de dirección.

    Retorna:
        - direccion_actual: La nueva dirección del jugador.
    """

    # Tecla W
    if keys[pygame.K_w]:
        # La tupla nos indica que horizontalmente (columnas) no hará nada (0) y
        # que verticalmente (filas) disminuirá el índice en el tablero (-1).
        return (0, -1)

    # Tecla S
    if keys[pygame.K_s]:
        # En este caso avanzará a través de las filas del tablero.
        return (0, 1)

    # Tecla A
    if keys[pygame.K_a]:
        # Retrocede por las columnas del tablero.
        return (-1, 0)

    # Tecla D
    if keys[pygame.K_d]:
        # Avanza por las columnas del tablero.
        return (1, 0)

    # Si no se presiona ninguna de las teclas anteriores, la dirección
    # será la misma que la anterior.
    return direccion_actual


def avanzar(tablero, pos_jugador, direccion):
    """
    Avanza el jugador un paso en la dirección dada.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - pos_jugador: Tupla con la posición actual (índice con
            estructura (columna, fila)) del jugador en el tablero.
        - direccion: Tupla con la dirección en la que está avanzando actualmente el jugador.

    Retorna:
        - (resultado, nueva_pos_jugador): Retorna el resultado que se obtiene
            al avanzar (derrota, victoria o "ok" (no cambia de pantalla)) y la nueva posición del jugador.
    """

    # Obtenemos los componentes "x" e "y" de cada tupla recibida
    # con información de la dirección y posición del jugador.
    dir_col, dir_fila = direccion
    ind_actual_col, ind_actual_fila = (
        pos_jugador  # Tupla (columna, fila) que representa los índices en el tablero.
    )

    # Aplicamos la dirección a la posición del jugador.
    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    # Verificamos que no haya choque con el borde del tablero.
    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        return "ok", pos_jugador

    # Obtenemos el elemento que se encuentre en el tablero en la nueva posición del jugador.
    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

    if pos_elem == OBSTACULO:
        return "ok", pos_jugador

    if pos_elem == DIAMANTE:
        tablero[ind_actual_fila][ind_actual_col] = VACIO
        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR       
        return "diamante", (ind_nueva_col, ind_nueva_fila)

    # Movimiento normal, si es que no encontramos manzana ni obstáculo.
    tablero[ind_actual_fila][ind_actual_col] = VACIO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

    return "ok", (ind_nueva_col, ind_nueva_fila)

def romper_roca(tablero, pos_jugador, direccion): #mecanica de mineria

    col, fila = pos_jugador

    dir_col, dir_fila = direccion

    objetivo_col = col + dir_col
    objetivo_fila = fila + dir_fila

    if not (
        0 <= objetivo_col < COLUMNAS
        and 0 <= objetivo_fila < FILAS
    ):
        return

    if tablero[objetivo_fila][objetivo_col] == OBSTACULO:
        tablero[objetivo_fila][objetivo_col] = VACIO

def reiniciar(nivel):
    """
    Crea un nuevo tablero y estado para una nueva partida.

    Retorna:
        - (tablero, pos_jugador): Tablero nuevo y la nueva posición aleatoria del jugador.
            pos_jugador corresponda a una tupla (columna, fila) donde columna y fila son índices
            de matriz tablero.
    """

    # Si se modifica constante FILAS o COLUMNAS al inicio, también
    # se debe modificar este arreglo de tablero con los valores correspondientes.
    # Esto puede ser mejorado usando dos bucles "for" anidados o comprensión de listas.

    tablero = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # Usando dos bucles "for" anidados se haría de la siguiente manera:
    # tablero = []
    # for _ in range(FILAS):
    #     fila_tablero = []
    #
    #     for _ in range(COLUMNAS):
    #         fila_tablero.append(VACIO)
    #
    #     tablero.append(fila_tablero)
    # Otra manera usando comprensión de listas:
    # tablero = [[VACIO] * COLUMNAS for _ in range(FILAS)]
    # El _ en el "for" indica que no usamos la variable con la que iteramos.

    poblar_tablero(tablero,nivel)

    # Colocamos al jugador en una posición aleatoria.
    pos_jugador = aparecer_aleatorio(tablero, JUGADOR)

    return tablero, pos_jugador


def mostrar_pantalla(screen, nombre_archivo):
    """
    Carga una imagen y la muestra escalada a la ventana.

    Parámetros:
        - screen: La pantalla donde colocaremos la imagen.
        - nombre_archivo: El nombre del archivo de la imagen.
    """

    ruta = os.path.join(DIR_PANTALLAS, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, screen.get_size())

        # Dibujamos la imagen en la pantalla en la coordenada (0, 0).
        screen.blit(imagen, (0, 0))

        # Refrescamos pantalla.
        pygame.display.flip()
    except FileNotFoundError:
        # Fallback de seguridad en caso de que las imágenes no existan aún
        screen.fill("black")
        pygame.display.flip()
        print(f"Advertencia: No se encontró la imagen {ruta}")


def main():
    pygame.init()

    # Establecemos la resolución de la pantalla.
    screen = pygame.display.set_mode((800, 800))

    # Establecemos el título de la ventana.
    pygame.display.set_caption("MINE IT ALL")
    fuente = pygame.font.SysFont(None, 40)
    running = True

    estado = ESTADO_INICIO
    tablero = []
    pos_jugador = (0, 0)
    direccion = (0, 0)
    ultima_direccion = (1, 0)
    tiempo_ultimo_mov = 0
    nivel = 1
    diamantes= 0

    mostrar_pantalla(screen, PANTALLA_INICIO)
    
    # Este es el bucle principal del juego, todo lo que sucede en el juego
    # está aquí.
    while running:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.KEYDOWN:
                if estado == ESTADO_JUGANDO and evento.key == pygame.K_e:
                    romper_roca(
                        tablero,
                        pos_jugador,
                        ultima_direccion
                    )
                    refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    fuente
                )

                if estado == ESTADO_INICIO:

                    if evento.key == pygame.K_SPACE:
                        nivel = 1
                        tablero, pos_jugador = reiniciar(nivel - 1)
                        diamantes = 0
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        refrescar_tablero(
                            screen,
                            tablero,
                            diamantes,
                            NIVELES[nivel - 1]["diamantes"],
                            fuente
                        )

                    elif evento.key == pygame.K_i:
                        estado = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(screen, PANTALLA_INSTRUCCIONES)

                elif estado == ESTADO_INSTRUCCIONES:
                    estado = ESTADO_INICIO
                    mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado in (ESTADO_DERROTA, ESTADO_VICTORIA):

                    if evento.key == pygame.K_r:

                        nivel = 1
                        tablero, pos_jugador = reiniciar(0)

                        diamantes = 0
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()

                        estado = ESTADO_JUGANDO

                        refrescar_tablero(
                            screen,
                            tablero,
                            diamantes,
                            NIVELES[0]["diamantes"],
                            fuente
                        )

                    elif evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)

        if estado == ESTADO_JUGANDO:
            # Movimiento del jugador con WASD mientras la tecla esté presionada
            # -Pan
            keys = pygame.key.get_pressed()
            if diamantes >= NIVELES[nivel - 1]["diamantes"]:
                nivel += 1
                if nivel > len(NIVELES):
                    estado = ESTADO_VICTORIA
                    mostrar_pantalla(screen, PANTALLA_VICTORIA)

                else:
                    diamantes = 0
                    tablero, pos_jugador = reiniciar(nivel - 1)
                    refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    fuente
                )
            direccion = (0, 0)

            if keys[pygame.K_w]:
                direccion = (0, -1)
                ultima_direccion = direccion

            elif keys[pygame.K_s]:
                direccion = (0, 1)
                ultima_direccion = direccion

            elif keys[pygame.K_a]:
                direccion = (-1, 0)
                ultima_direccion = direccion

            elif keys[pygame.K_d]:
                direccion = (1, 0)
                ultima_direccion = direccion


            tiempo_actual = pygame.time.get_ticks()

            if direccion != (0, 0) and tiempo_actual - tiempo_ultimo_mov >= RETRASO:

                resultado, pos_jugador = avanzar(
                    tablero,
                    pos_jugador,
                    direccion
                )

                if resultado == "derrota":
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)

                elif resultado == "diamante":
                    diamantes += 1
                    print("Diamantes:", diamantes)
                    refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    fuente
                )

                else:
                    refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    fuente
                )
                tiempo_ultimo_mov = tiempo_actual        
pygame.quit()

if __name__ == "__main__":
    main()
