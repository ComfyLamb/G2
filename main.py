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
ESTADO_PAUSA = "pausa"

#pantallas
DIR_PANTALLAS = os.path.join(os.path.dirname(__file__), "data", "pantallas") #busca carpeta de pantallas
PANTALLA_INICIO = "pantalla_inicio.bmp"
PANTALLA_INSTRUCCIONES = "pantalla_instrucciones.bmp"
PANTALLA_VICTORIA = "pantalla_victoria.bmp"
PANTALLA_DERROTA = "pantalla_derrota.bmp"
PANTALLA_PAUSA = "pantalla_pausa.bmp"

#sprites
DIR_SPRITES = os.path.join(os.path.dirname(__file__), "data", "sprites") #busca carpeta de sprites
SPRITE_MINERO = "minero.png"
SPRITE_TOPO = "topo.png"
SPRITE_ROCA = "roca.png"
SPRITE_DIAMANTE = "diamante.png"
SPRITE_MANZANA = "manzana.png"
SPRITE_LAVA = "lava.png"

#sonidos
DIR_SONIDOS = os.path.join(os.path.dirname(__file__), "data", "sonidos") #busca carpeta de sfx
SONIDO_DERROTA = "derrota.wav"
SONIDO_VICTORIA = "victoria.wav"
SONIDO_DIAMANTE = "diamante.wav"
SONIDO_MANZANA = "manzana.wav"
SONIDO_ROCA = "roca.wav"

#música
DIR_MUSICA = os.path.join(os.path.dirname(__file__), "data", "musica") #busca carpeta de soundtracks
MUSICA_INICIO = "musica_inicio.mp3"
MUSICA_VICTORIA = "musica_victoria.mp3"
MUSICA_DERROTA = "musica_derrota.mp3"
MUSICA_JUEGO = "musica_juego.mp3"

#delays de movimiento usados en el movimiento del jugador o del topo
RETRASO = 200
RETRASO2 = 100

#códigos de elementos
VACIO = 0
ROCA = 1
JUGADOR = 2
DIAMANTE = 3
TOPO = 4
MANZANA = 5
LAVA = 6

#cantidad de cosas en cada nivel
NIVELES = [
    {
        "diamantes": 5, #nivel 1: 5 diamantes, 100 rocas, 1 manzana, 3 charcos de lava, 1 topo
        "rocas": 100,
        "topo": 1,
        "manzana": 1,
        "lava": 3
    },
    {
        "diamantes": 5, #nivel 2: 5 diamantes, 125 rocas, 1 manzana, 5 charcos de lava, 1 topo
        "rocas": 125,
        "topo": 1,
        "manzana": 1,
        "lava": 5
    },
    {
        "diamantes": 5, #nivel 3: 5 diamantes, 150 rocas, 1 manzana, 9 charcos de lava, 1 topo
        "rocas": 150,
        "topo": 1,
        "manzana": 1,
        "lava": 9
    },
    {
        "diamantes": 1,
        "rocas": 150,
        "topo": 1,
        "manzana": 0,
        "lava": 25
    }
]

#tablero, importante no cambiar ya que el tamaño de los sprites estan pensados para que quepan en cada casilla
FILAS = 15
COLUMNAS = 15


def aparecer_aleatorio(tablero, id_elem): #llama a la matriz y luego a la id de los elementos

    vacios = [] #lista donde se guardan las casillas de "vacio"
    for fila in range(FILAS): #recorre cada fila
        for columna in range(COLUMNAS): #recorre cada columna
            elem_pos = tablero[fila][columna]
            if elem_pos == VACIO:
                if id_elem in (JUGADOR, TOPO, DIAMANTE, MANZANA):
                    if posicion_segura(tablero, columna, fila):
                        vacios.append((columna, fila))
                else:
                    vacios.append((columna, fila))
    if len(vacios) == 0:
        return -1, -1
    columna, fila = random.choice(vacios)
    tablero[fila][columna] = id_elem
    return columna, fila

#funcion que hace que el jugador, el diamante, la manzana y el topo no aparezcan encerrados de lava
def posicion_segura(tablero, columna, fila):

    cantidad_lava = 0

    for dir_col, dir_fila in [
        (0,1),
        (0,-1),
        (1,0),
        (-1,0)
    ]:

        nueva_col = columna + dir_col
        nueva_fila = fila + dir_fila

        if (
            0 <= nueva_col < COLUMNAS
            and 0 <= nueva_fila < FILAS
        ):
            if tablero[nueva_fila][nueva_col] == LAVA:
                cantidad_lava += 1

    return cantidad_lava < 3

def poblar_tablero(tablero, nivel):

    print("Nivel:", nivel + 1) #muestra en la consola que nivel se está jugando, el +1 porque python cuenta desde 0
    config = NIVELES[nivel]

    for i in range(config["lava"]): #genera la lava
        aparecer_aleatorio(tablero, LAVA)

    for i in range(config["rocas"]): #genera las rocas
        aparecer_aleatorio(tablero, ROCA)

    aparecer_aleatorio(tablero, DIAMANTE) #genera un solo diamante
    
    pos_topo = None
    for i in range(config["topo"]): #genera al topo
        pos_topo = aparecer_aleatorio(tablero, TOPO)

    for i in range(config["manzana"]): #genera la manzana
        aparecer_aleatorio(tablero, MANZANA)
    
    return pos_topo

def refrescar_tablero(
        screen,
        tablero,
        diamantes,
        objetivo,
        oxigeno,
        fuente,
        sprites
        ):

    screen.fill("gray20") #color base del tablero

    alto_elem = screen.get_height() / FILAS
    ancho_elem = screen.get_width() / COLUMNAS

    pos_y = 0

    for i in range(FILAS):
        pos_x = 0
        for j in range(COLUMNAS):
            elemento = tablero[i][j]

            if elemento in sprites:
                screen.blit(
                    pygame.transform.scale(
                        sprites[elemento],
                        (int(ancho_elem), int(alto_elem))
                    ),
                    (pos_x, pos_y)
                )

            pos_x += ancho_elem
        pos_y += alto_elem
    
    #muestra el texto de diamantes arriba a la izquierda de la pantalla
    texto_diamantes = fuente.render(
        f"Diamantes: {diamantes}/{objetivo}",
        True,
        (0, 255, 255) #color
    )

    #muestra el texto de ox+ígeno debajo del de diamantes
    texto_oxigeno = fuente.render(
        f"Oxígeno: {oxigeno}",
        True,
        (255,255,255) #color
)

    screen.blit(texto_diamantes, (10, 10))
    screen.blit(texto_oxigeno, (10, 50))
    pygame.display.flip()

def avanzar(tablero, pos_jugador, direccion):

    dir_col, dir_fila = direccion
    ind_actual_col, ind_actual_fila = (
        pos_jugador
    )

    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        return "ok", pos_jugador

    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

    if pos_elem == TOPO: #si el jugador colisiona con el topo, pierde
        return "derrota", pos_jugador

    if pos_elem == ROCA: #si el jugador colisiona con una roca, no pasa nada
        return "ok", pos_jugador
    
    if pos_elem == LAVA: #si el jugador colisiona con lava, pierde
        return "derrota", pos_jugador
    
    if pos_elem == MANZANA: #si el jugador colisiona con la manzana, la casilla se reemplaza con "vacio"
        tablero[ind_actual_fila][ind_actual_col] = VACIO
        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR
        return "manzana", (ind_nueva_col, ind_nueva_fila)

    if pos_elem == DIAMANTE: #si el jugador colisiona con el diamante, la casilla se reemplaza con "vacio"
        tablero[ind_actual_fila][ind_actual_col] = VACIO
        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR       
        return "diamante", (ind_nueva_col, ind_nueva_fila)

    tablero[ind_actual_fila][ind_actual_col] = VACIO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

    return "ok", (ind_nueva_col, ind_nueva_fila)

#mecánica de minería
def romper_roca(tablero, pos_jugador, direccion): #llama al tablero, la posición del jugador y luego la dirección

    col, fila = pos_jugador
    dir_col, dir_fila = direccion

    objetivo_col = col + dir_col
    objetivo_fila = fila + dir_fila

    if not (
        0 <= objetivo_col < COLUMNAS
        and 0 <= objetivo_fila < FILAS
    ):
        return False
    

    if tablero[objetivo_fila][objetivo_col] == ROCA: #si el objetivo es una roca:
        tablero[objetivo_fila][objetivo_col] = VACIO #lo combierte en "vacio"
        return True
    
    return False

#movimiento del topo
def mover_topo(tablero, pos_topo): #llama al tablero y a la posición actual del topo

    col, fila = pos_topo

    movimientos = [ #señala cuánto se puede llegar a mover el topo, en este caso de a 1 casilla de distancia
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]

    random.shuffle(movimientos) #movimiento aleatorio

    for dir_col, dir_fila in movimientos:

        nueva_col = col + dir_col
        nueva_fila = fila + dir_fila

        if not (
            0 <= nueva_col < COLUMNAS
            and 0 <= nueva_fila < FILAS
        ):
            continue

        if tablero[nueva_fila][nueva_col] in (VACIO, JUGADOR, ROCA): #solo se puede mover en "vacio", "jugador", "roca"

            if tablero[nueva_fila][nueva_col] == JUGADOR:
                tablero[fila][col] = VACIO
                tablero[nueva_fila][nueva_col] = TOPO
                return "derrota" #si el topo toca al jugador, retorna derrota

            tablero[fila][col] = VACIO
            tablero[nueva_fila][nueva_col] = TOPO

            return (nueva_col, nueva_fila)

    return pos_topo

def reiniciar(nivel):

    tablero = [
        [VACIO for _ in range(COLUMNAS)]
        for _ in range(FILAS)
    ]

    pos_topo = poblar_tablero(tablero,nivel)

    pos_jugador = aparecer_aleatorio(tablero, JUGADOR)

    return tablero, pos_jugador, pos_topo


def mostrar_pantalla(screen, nombre_archivo):

    ruta = os.path.join(DIR_PANTALLAS, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, screen.get_size())

        screen.blit(imagen, (0, 0))

        pygame.display.flip()
    except FileNotFoundError:

        screen.fill("black")
        pygame.display.flip()
        print("No se encontró imagen") #aviso de posible error

def reproducir_musica(nombre_archivo, loop=-1):
    ruta = os.path.join(DIR_MUSICA, nombre_archivo)

    try:
        pygame.mixer.music.load(ruta) #inicia el soundtrack
        pygame.mixer.music.set_volume(0.4) #ajusta el volumen del soundtrack al 40%
        pygame.mixer.music.play(loop) #reinicia el soundtrack de forma infinita
    except Exception as e:
        print("No se encontró música", e) #aviso de posible error

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 800))

    sprite_lava = pygame.image.load(
        os.path.join(DIR_SPRITES, SPRITE_LAVA)
    )
    sprite_roca = pygame.image.load(
        os.path.join(DIR_SPRITES, SPRITE_ROCA)
    )
    sprite_topo = pygame.image.load(
        os.path.join(DIR_SPRITES, SPRITE_TOPO)
    )
    sprite_manzana = pygame.image.load(
        os.path.join(DIR_SPRITES, SPRITE_MANZANA)
    )
    sprite_diamante = pygame.image.load(
        os.path.join(DIR_SPRITES, SPRITE_DIAMANTE)
    )
    sprite_minero = pygame.image.load(
        os.path.join(DIR_SPRITES, SPRITE_MINERO)
    )
    sprites = {
        ROCA: sprite_roca,
        JUGADOR: sprite_minero,
        MANZANA: sprite_manzana,
        TOPO: sprite_topo,
        DIAMANTE: sprite_diamante,
        LAVA: sprite_lava
    }
    

    sonido_manzana = pygame.mixer.Sound(
        os.path.join(
            DIR_SONIDOS,
            SONIDO_MANZANA
        )
    )
    sonido_diamante = pygame.mixer.Sound(
        os.path.join(
            DIR_SONIDOS,
            SONIDO_DIAMANTE
        )
    )
    sonido_victoria = pygame.mixer.Sound(
        os.path.join(
            DIR_SONIDOS,
            SONIDO_VICTORIA
        )
    )
    sonido_derrota = pygame.mixer.Sound(
        os.path.join(
            DIR_SONIDOS,
            SONIDO_DERROTA
        )
    )
    sonido_roca = pygame.mixer.Sound(
        os.path.join(
            DIR_SONIDOS,
            SONIDO_ROCA
        )
    )

    pygame.display.set_caption("MINE IT ALL")
    fuente = pygame.font.SysFont(None, 40)
    running = True

    estado = ESTADO_INICIO
    tablero = []
    pos_jugador = (0, 0)
    pos_topo = (0, 0)
    direccion = (0, 0)
    ultima_direccion = (1, 0)
    tiempo_ultimo_mov = 0
    nivel = 1
    diamantes= 0
    RETRASO_ACTUAL = RETRASO
    turbo_activo = False
    tiempo_turbo = 0
    tiempo_ultimo_topo = 0
    RETRASO_TOPO = 200
    OXIGENO_MAX = 30
    oxigeno = OXIGENO_MAX
    tiempo_ultimo_oxigeno = pygame.time.get_ticks()


    mostrar_pantalla(screen, PANTALLA_INICIO)
    reproducir_musica(MUSICA_INICIO)
    
    while running:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.KEYDOWN:

                #tecla de admin para pasar instantaneamente de nivel
                if estado == ESTADO_JUGANDO and evento.key == pygame.K_n:
                    diamantes = NIVELES[nivel - 1]["diamantes"]

                #vuelve al inicio con la tecla escape durante el juego
                if estado == ESTADO_JUGANDO and evento.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    reproducir_musica(MUSICA_INICIO)
                    estado = ESTADO_INICIO
                    mostrar_pantalla(screen, PANTALLA_INICIO)
                    continue #este "continue" es importante para que no se cierre el juego instantaneamente

                if estado == ESTADO_JUGANDO and evento.key == pygame.K_e:
                    roca_rota=romper_roca(
                        tablero,
                        pos_jugador,
                        ultima_direccion
                    )
                    if roca_rota:
                        sonido_roca.play()
                        
                    refrescar_tablero(
                        screen,
                        tablero,
                        diamantes,
                        NIVELES[nivel - 1]["diamantes"],
                        oxigeno,
                        fuente,
                        sprites
                    )

                if estado == ESTADO_INICIO:
                    
                    if evento.key == pygame.K_ESCAPE:
                        running = False

                    if evento.key == pygame.K_SPACE:
                        OXIGENO_MAX = 30
                        oxigeno = OXIGENO_MAX
                        tiempo_ultimo_oxigeno = pygame.time.get_ticks()
                        nivel = 1
                        tablero, pos_jugador, pos_topo = reiniciar(nivel - 1)
                        if nivel == 1:
                            OXIGENO_MAX = 30
                        elif nivel == 2:
                            OXIGENO_MAX = 25
                        elif nivel == 3:
                            OXIGENO_MAX = 20

                        oxigeno = OXIGENO_MAX
                        tiempo_ultimo_oxigeno = pygame.time.get_ticks()
                        diamantes = 0
                        direccion = (0, 0)
                        RETRASO_ACTUAL = RETRASO
                        turbo_activo = False
                        tiempo_turbo = 0
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        reproducir_musica(MUSICA_JUEGO)
                        refrescar_tablero(
                            screen,
                            tablero,
                            diamantes,
                            NIVELES[nivel - 1]["diamantes"],
                            oxigeno,
                            fuente,
                            sprites
                        )

                    elif evento.key == pygame.K_i:
                        estado = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(screen, PANTALLA_INSTRUCCIONES)

                elif estado == ESTADO_INSTRUCCIONES:
                    estado = ESTADO_INICIO
                    mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado in (ESTADO_DERROTA, ESTADO_VICTORIA):

                    if evento.key == pygame.K_r:

                        OXIGENO_MAX = 30
                        oxigeno = OXIGENO_MAX
                        tiempo_ultimo_oxigeno = pygame.time.get_ticks()
                        nivel = 1
                        tablero, pos_jugador, pos_topo = reiniciar(0)

                        diamantes = 0
                        direccion = (0, 0)
                        RETRASO_ACTUAL = RETRASO
                        turbo_activo = False
                        tiempo_turbo = 0
                        tiempo_ultimo_mov = pygame.time.get_ticks()

                        estado = ESTADO_JUGANDO
                        reproducir_musica(MUSICA_JUEGO)

                        refrescar_tablero(
                            screen,
                            tablero,
                            diamantes,
                            NIVELES[0]["diamantes"],
                            oxigeno,
                            fuente,
                            sprites
                        )

                    elif evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)
                        reproducir_musica(MUSICA_INICIO)

        if estado == ESTADO_JUGANDO:
            keys = pygame.key.get_pressed()

            if diamantes >= NIVELES[nivel - 1]["diamantes"]:
                nivel += 1

                if nivel > len(NIVELES):
                    pygame.mixer.music.stop()
                    sonido_victoria.play()
                    pygame.time.wait(4500)
                    reproducir_musica(MUSICA_VICTORIA)
                    estado = ESTADO_VICTORIA
                    mostrar_pantalla(screen, PANTALLA_VICTORIA)
                    continue

                else:
                    diamantes = 0
                    tablero, pos_jugador, pos_topo = reiniciar(nivel - 1)
                    oxigeno = OXIGENO_MAX
                    tiempo_ultimo_oxigeno = pygame.time.get_ticks()
                    tiempo_ultimo_topo = pygame.time.get_ticks()
                    refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    oxigeno,
                    fuente,
                    sprites
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

            if tiempo_actual - tiempo_ultimo_oxigeno >= 1000:
                oxigeno -= 1
                tiempo_ultimo_oxigeno = tiempo_actual

                if oxigeno <= 0:
                    pygame.mixer.music.stop()
                    sonido_derrota.play()
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                    pygame.time.wait(4500)
                    reproducir_musica(MUSICA_DERROTA, 0)

            if tiempo_actual - tiempo_ultimo_topo >= RETRASO_TOPO:

                resultado_topo = mover_topo(
                    tablero,
                    pos_topo
                )
                if resultado_topo == "derrota":
                    pygame.mixer.music.stop()
                    sonido_derrota.play()
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                    pygame.time.wait(4500)
                    reproducir_musica(MUSICA_DERROTA, 0)

                    continue

                pos_topo = resultado_topo

                refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    oxigeno,
                    fuente,
                    sprites
                )
                tiempo_ultimo_topo = tiempo_actual
                

            if turbo_activo:
                if tiempo_actual - tiempo_turbo >= 5000:  #5 segundos
                    turbo_activo = False
                    RETRASO_ACTUAL = RETRASO

            if direccion != (0, 0) and tiempo_actual - tiempo_ultimo_mov >= RETRASO_ACTUAL:
                resultado, pos_jugador = avanzar(
                    tablero,
                    pos_jugador,
                    direccion
                )

                if resultado == "derrota":
                    pygame.mixer.music.stop()
                    sonido_derrota.play()
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                    pygame.time.wait(4500)
                    reproducir_musica(MUSICA_DERROTA, 0)

                elif resultado == "diamante":
                    sonido_diamante.play()
                    diamantes += 1
                    if diamantes < NIVELES[nivel - 1]["diamantes"]:
                        aparecer_aleatorio(tablero, DIAMANTE)
                    print("Diamantes:", diamantes)

                    refrescar_tablero(
                        screen,
                        tablero,
                        diamantes,
                        NIVELES[nivel - 1]["diamantes"],
                        oxigeno,
                        fuente,
                        sprites
                    )

                elif resultado == "manzana":
                    sonido_manzana.play() #carga el sonido de la manzana
                    turbo_activo = True #actualiza el estado del turbo
                    tiempo_turbo = pygame.time.get_ticks()
                    RETRASO_ACTUAL = RETRASO2
                    refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    oxigeno,
                    fuente,
                    sprites
                )

                else:
                    refrescar_tablero(
                    screen,
                    tablero,
                    diamantes,
                    NIVELES[nivel - 1]["diamantes"],
                    oxigeno,
                    fuente,
                    sprites
                )
                tiempo_ultimo_mov = tiempo_actual        
    pygame.quit()

if __name__ == "__main__":
    main()
