import random
import pygame
from PyOpenGLtoolbox import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Dimensiones de la pantalla
anchopantalla = 1750
altopantalla = 1000

# Textura seleccionada
textura_seleccionada = ""

keys = {
    pygame.K_w: False,
    pygame.K_s: False,
    pygame.K_a: False,
    pygame.K_d: False,
    pygame.K_SPACE: False,
    pygame.K_LSHIFT: False,
    pygame.K_RSHIFT: False,
    pygame.K_u: False,
    pygame.K_r: False,
    pygame.K_q: False,
    pygame.K_ESCAPE: False,
    pygame.K_z: False
}

# Base del piso
base_piso = 180

# Piezas de mapa encontradas
piezasMapa = 0


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def get_r(self):
        return self.r

    def get_g(self):
        return self.g

    def get_b(self):
        return self.b


# Inicializar los colores
rojo = Color(1.0, 0.0, 0.0)
verde = Color(0.0, 1.0, 0.0)
azul = Color(0.0, 0.0, 1.0)
amarillo = Color(1.0, 1.0, 0)
magenta = Color(1.0, 0.0, 1.0)
cyan = Color(0.0, 1.0, 1.0)
gris = Color(0.5, 0.5, 0.5)
grisClaro = Color(0.75, 0.75, 0.75)
blanco = Color(1.0, 1.0, 1.0)
negro = Color(0.0, 0.0, 0.0)


class Textura:
    def __init__(self, archivo):
        self.archivo = archivo
        self.textura = None
        self.texture_id = glGenTextures(1)  # Generate a unique texture ID

    def cargarTextura(self):
        if not os.path.isfile(self.archivo):
            print(f"Error: El archivo no existe: {self.archivo}")
            return

        try:
            imagen = pygame.image.load(self.archivo)
            self.width, self.height = imagen.get_size()
            print(f"Cargando textura {self.archivo} ({self.width}x{self.height})")

            self.textura = pygame.image.tostring(imagen, "RGBA", True)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.textura)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            # Habilitar la mezcla de colores para manejar la transparencia
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            print(f"Textura cargada con ID {self.texture_id}")

        except Exception as e:
            print(f"Error al cargar la textura: {e}")

    def aplicarTextura(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)  # Bind the unique texture ID


# Diccionario de texturas
texturas = {
    "dirt1": "./textures/Blocks/dirt1.png",
    "dirt2": "./textures/Blocks/dirt2.png",
    "dirt_grass1": "./textures/Blocks/dirt_grass1.png",
    "dirt_grass2": "./textures/Blocks/dirt_grass2.png",
    "grass1": "./textures/Blocks/grass1.png",
    "grass2": "./textures/Blocks/grass2.png",
    "scene1": "./textures/scene1.png",
    "scene2": "./textures/scene2.png",
    "scene3": "./textures/scene3.png",
    "scene4": "./textures/scene4.png",
    "scene5": "./textures/scene5.png",
    "knight_walk1": "./textures/Knight/Walk/Knight_Walk1.png",
    "knight_walk2": "./textures/Knight/Walk/Knight_Walk2.png",
    "knight_walk3": "./textures/Knight/Walk/Knight_Walk3.png",
    "knight_walk4": "./textures/Knight/Walk/Knight_Walk4.png",
    "knight_walk5": "./textures/Knight/Walk/Knight_Walk5.png",
    "knight_walk6": "./textures/Knight/Walk/Knight_Walk6.png",
    "knight_walk7": "./textures/Knight/Walk/Knight_Walk7.png",
    "knight_walk8": "./textures/Knight/Walk/Knight_Walk8.png",
    "knight_run1": "./textures/Knight/Run/Knight_Run1.png",
    "knight_run2": "./textures/Knight/Run/Knight_Run2.png",
    "knight_run3": "./textures/Knight/Run/Knight_Run3.png",
    "knight_run4": "./textures/Knight/Run/Knight_Run4.png",
    "knight_run5": "./textures/Knight/Run/Knight_Run5.png",
    "knight_run6": "./textures/Knight/Run/Knight_Run6.png",
    "knight_run7": "./textures/Knight/Run/Knight_Run7.png",
    "knight_idle1": "./textures/Knight/Idle/Knight_Idle1.png",
    "knight_idle2": "./textures/Knight/Idle/Knight_Idle2.png",
    "knight_idle3": "./textures/Knight/Idle/Knight_Idle3.png",
    "knight_idle4": "./textures/Knight/Idle/Knight_Idle4.png",
    "knight_hurt1": "./textures/Knight/Hurt/Knight_Hurt1.png",
    "knight_hurt2": "./textures/Knight/Hurt/Knight_Hurt2.png",
    "knight_attack1": "./textures/Knight/Attack/Knight_Attack1.png",
    "knight_attack2": "./textures/Knight/Attack/Knight_Attack2.png",
    "knight_attack3": "./textures/Knight/Attack/Knight_Attack3.png",
    "knight_attack4": "./textures/Knight/Attack/Knight_Attack4.png",
    "knight_attack5": "./textures/Knight/Attack/Knight_Attack5.png",
    "princess_idle1": "./textures/Princess/Idle/Princess_Idle1.png",
    "princess_idle2": "./textures/Princess/Idle/Princess_Idle2.png",
    "princess_idle3": "./textures/Princess/Idle/Princess_Idle3.png",
    "princess_idle4": "./textures/Princess/Idle/Princess_Idle4.png",
    "princess_idle5": "./textures/Princess/Idle/Princess_Idle5.png",
    "princess_idle6": "./textures/Princess/Idle/Princess_Idle6.png",
    "princess_idle7": "./textures/Princess/Idle/Princess_Idle7.png",
    "caja_1": "./textures/Caja/caja1.png",
    "caja_2": "./textures/Caja/caja3.png",
    "mapa_1": "./textures/Map/map1.png",
    "mapa_2": "./textures/Map/map2.png",
    "mapa_3": "./textures/Map/map3.png",
    "mapa_4": "./textures/Map/map4.png",
    "game_over": "./textures/game_over.png",
}


def draw_rectangle(x, y, width, height, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)  # Reset color to white


class Fondo:
    def __init__(self, archivo):
        self.archivo = archivo
        self.textura = None
        self.texture_id = glGenTextures(1)  # Generate a unique texture ID

    def cargarTextura(self):
        if not os.path.isfile(self.archivo):
            print(f"Error: El archivo no existe: {self.archivo}")
            return

        try:
            imagen = pygame.image.load(self.archivo)
            self.width, self.height = imagen.get_size()
            print(f"Cargando textura de fondo {self.archivo} ({self.width}x{self.height})")

            self.textura = pygame.image.tostring(imagen, "RGBA", True)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.textura)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            print(f"Textura de fondo cargada con ID {self.texture_id}")

        except Exception as e:
            print(f"Error al cargar la textura de fondo: {e}")

    def dibujarFondo(self):
        glEnable(GL_TEXTURE_2D)  # Habilitar texturas
        glBindTexture(GL_TEXTURE_2D, self.texture_id)  # Bind the unique texture ID

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-anchopantalla, -altopantalla)

        glTexCoord2f(1.0, 0.0)
        glVertex2f(anchopantalla, -altopantalla)

        glTexCoord2f(1.0, 1.0)
        glVertex2f(anchopantalla, altopantalla)

        glTexCoord2f(0.0, 1.0)
        glVertex2f(-anchopantalla, altopantalla)
        glEnd()

        glDisable(GL_TEXTURE_2D)  # Deshabilitar texturas


class Bloque:
    def __init__(self, lado, textura: Textura):
        self.lado = lado
        self.textura = textura

    def get_lado(self):
        return self.lado

    def get_textura(self):
        return self.textura

    def dibujarBloque(self):
        lado = self.lado
        textura = self.textura

        # Habilitar texturas
        glEnable(GL_TEXTURE_2D)

        # Aplicar la textura de la cara
        textura.aplicarTextura()

        # Dibujar el bloque 2D
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-lado / 2, -lado / 2)

        glTexCoord2f(1.0, 0.0)
        glVertex2f(lado / 2, -lado / 2)

        glTexCoord2f(1.0, 1.0)
        glVertex2f(lado / 2, lado / 2)

        glTexCoord2f(0.0, 1.0)
        glVertex2f(-lado / 2, lado / 2)
        glEnd()

        self.disable = glDisable(GL_TEXTURE_2D)


class Personaje:
    def __init__(self, x, y, factor_x, factor_y, lado, texturas_caminando, texturas_idle, texturas_corriendo,
                 texturas_hurt, texturas_atacando, vidas):
        self.x = x
        self.y = y
        self.factor_x = factor_x
        self.factor_y = factor_y
        self.lado = lado
        self.texturas_caminando = texturas_caminando
        self.texturas_idle = texturas_idle
        self.texturas_corriendo = texturas_corriendo
        self.texturas_hurt = texturas_hurt
        self.texturas_atacando = texturas_atacando
        self.vidas = vidas
        self.vel_y = 0
        self.en_el_aire = False
        self.direccion = 1  # 1 for right, -1 for left
        self.frame = 0
        self.frame_rate = 0  # Change frame every 5 updates
        self.frame_counter = 0
        self.velocidad_movimiento = 0
        self.estado = "idle"  # "idle" or "walking"
        self.invulnerable = False  # Estado de invulnerabilidad
        self.invulnerable_timer = 0  # Temporizador para la invulnerabilidad

    def dibujar(self):
        # Habilitar texturas
        glEnable(GL_TEXTURE_2D)

        # Aplicar la textura correcta según el estado
        if self.estado == "walking":
            self.texturas_caminando[self.frame % len(self.texturas_caminando)].aplicarTextura()
        elif self.estado == "idle":
            self.texturas_idle[self.frame % len(self.texturas_idle)].aplicarTextura()
        elif self.estado == "running":
            self.texturas_corriendo[self.frame % len(self.texturas_corriendo)].aplicarTextura()
        elif self.estado == "hurt":
            self.texturas_hurt[self.frame % len(self.texturas_hurt)].aplicarTextura()
        elif self.estado == "attacking":
            self.texturas_atacando[self.frame % len(self.texturas_atacando)].aplicarTextura()

        # Impresión de depuración
        # print(f"Estado: {self.estado}, Frame: {self.frame}")

        # Aplicar la escala para el flip
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glScalef(self.direccion, 1, 1)  # Flip the sprite based on direction
        glTranslatef(-self.x, -self.y, 0)

        # Dibujar el personaje como un cuadrado
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.x - self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x + self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x - self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Dibujar el area_ataque
        # if self.estado == "attacking":
        #     area_ataque = {
        #         "x": self.x - 50 + (self.lado / 2 * self.direccion),  # Ajusta la posición según la dirección
        #         "y": self.y - 80,  # Ajusta la altura si es necesario
        #         "width": 50,  # Ancho del área de ataque
        #         "height": 50  # Alto del área de ataque
        #     }
        #     draw_rectangle(area_ataque["x"], area_ataque["y"], area_ataque["width"], area_ataque["height"],
        #                    (1.0, 0.0, 0.0))

    def mover_izquierda(self):
        self.frame_rate = 15
        self.velocidad_movimiento = 6
        if self.x - self.lado / 2 - self.velocidad_movimiento >= -anchopantalla:
            self.x -= self.velocidad_movimiento
            self.direccion = -1  # Set direction to left
            self.estado = "walking"
            self.actualizar_animacion()

    def mover_derecha(self):
        self.frame_rate = 15
        self.velocidad_movimiento = 6
        if self.x + self.lado / 2 + self.velocidad_movimiento <= anchopantalla:
            self.x += self.velocidad_movimiento
            self.direccion = 1  # Set direction to right
            self.estado = "walking"
            self.actualizar_animacion()

    def correr_izquierda(self):
        self.frame_rate = 7
        self.velocidad_movimiento = 10
        if self.x - self.lado / 2 - self.velocidad_movimiento >= -anchopantalla:
            self.x -= self.velocidad_movimiento
            self.direccion = -1  # Set direction to left
            self.estado = "running"
            self.actualizar_animacion()

    def correr_derecha(self):
        self.frame_rate = 7
        self.velocidad_movimiento = 10
        if self.x + self.lado / 2 + self.velocidad_movimiento <= anchopantalla:
            self.x += self.velocidad_movimiento
            self.direccion = 1  # Set direction to right
            self.estado = "running"
            self.actualizar_animacion()

    def idle(self):
        self.frame_rate = 28
        self.estado = "idle"
        self.actualizar_animacion()

    def hurt(self):
        if self.vidas > 0:
            self.vidas -= 1
            self.estado = "hurt"
            self.frame = 0  # Reiniciar el frame para comenzar la animación desde el inicio
            # Reproducir el audio de daño
            audio_hurt.play()
        elif self.vidas == 0:
            game_over_screen()

    def atacar(self, cajas):
        self.frame_rate = 15
        self.estado = "attacking"
        self.actualizar_animacion()

        # Definir el área de ataque
        area_ataque = {
            "x": self.x - 50 + (self.lado / 2 * self.direccion),  # Ajusta la posición según la dirección
            "y": self.y - 80,  # Ajusta la altura si es necesario
            "width": 50,  # Ancho del área de ataque
            "height": 50  # Alto del área de ataque
        }

        # Verificar colisiones con las cajas
        for caja in cajas:
            if (area_ataque["x"] < caja.x + caja.lado / 2 and
                    area_ataque["x"] + area_ataque["width"] > caja.x - caja.lado / 2 and
                    area_ataque["y"] < caja.y + caja.lado / 2 and
                    area_ataque["y"] + area_ataque["height"] > caja.y - caja.lado / 2):
                caja.golpear()  # Cambiar el estado de la caja

    # Miscellaneous method
    def teletransportar(self, x, y):
        self.x = x
        self.y = y

    def saltar(self, fuerza):
        if not self.en_el_aire:
            self.vel_y = fuerza
            self.en_el_aire = True

    def actualizar(self, gravedad):
        if self.invulnerable:
            self.invulnerable_timer -= 1  # Reducir el temporizador de invulnerabilidad
            if self.invulnerable_timer <= 0:
                self.invulnerable = False  # Desactivar invulnerabilidad

        # Aplicar gravedad si está en el aire
        if self.en_el_aire:
            self.y += self.vel_y
            self.vel_y -= gravedad

            # Verificar si el personaje ha caído al suelo
            if self.y <= base_piso:
                self.y = base_piso
                self.en_el_aire = False
                self.vel_y = 0

    def actualizar_animacion(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            if self.estado == "hurt":
                self.frame += 1
                if self.frame >= len(self.texturas_hurt):
                    self.frame = 0  # Reiniciar el frame si la animación ha terminado
                    self.estado = "idle"
            elif self.estado == "walking":
                self.frame = (self.frame + 1) % len(self.texturas_caminando)
            elif self.estado == "idle":
                self.frame = (self.frame + 1) % len(self.texturas_idle)
            elif self.estado == "running":
                self.frame = (self.frame + 1) % len(self.texturas_corriendo)
            elif self.estado == "attacking":
                self.frame += 1
                if self.frame >= len(self.texturas_atacando):
                    self.frame = 0  # Reiniciar el frame si la animación ha terminado
                    self.estado = "idle"
            self.frame_counter = 0


class CajaRompible:
    def __init__(self, x, y, factor_x, factor_y, lado, texturas, estado, trampa):
        self.x = x
        self.y = y
        self.factor_x = factor_x
        self.factor_y = factor_y
        self.lado = lado
        self.texturas = texturas
        self.estado = estado
        self.trampa = trampa
        self.fragmento_otorgado = False  # Añadir un flag para controlar la entrega del fragmento

    def dibujar(self):
        # Habilitar texturas
        glEnable(GL_TEXTURE_2D)

        # Aplicar la textura correcta según el estado
        if self.estado == "saludable":
            # Aplicar la textura 1
            self.texturas[0].aplicarTextura()
        elif self.estado == "rota":
            self.texturas[1].aplicarTextura()

        # Aplicar la escala para el flip
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glTranslatef(-self.x, -self.y, 0)

        # Dibujar el personaje como un cuadrado
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.x - self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x + self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x - self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Dibujar borde rojo si es trampa
        # if self.trampa:
        #     glColor3f(1.0, 0.0, 0.0)  # Color rojo
        #     glLineWidth(3)  # Ancho de línea
        #     glBegin(GL_LINE_LOOP)
        #     glVertex2f(self.x - self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        #     glVertex2f(self.x + self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        #     glVertex2f(self.x + self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        #     glVertex2f(self.x - self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        #     glEnd()
        #     glColor3f(1.0, 1.0, 1.0)  # Reset color to white

    def golpear(self):
        if self.estado == "saludable":
            self.estado = "rota"
            if not self.fragmento_otorgado:  # Verificar si ya se otorgó el fragmento
                self.fragmento_otorgado = True  # Marcar como otorgado
                self.rota()

    def rota(self):
        self.estado = "rota"
        if self.trampa:
            personaje.hurt()
        else:
            self.obtenerFragmentoMapa()

    def obtenerFragmentoMapa(self):
        global piezasMapa, fondo, cajas
        piezasMapa += 1
        audio_map_pickup.play()

        # Actualizar la textura de fondo según el número de piezas de mapa
        if piezasMapa == 1:
            fondo = Fondo(texturas["scene2"].archivo)
            personaje.teletransportar(-anchopantalla + 100, 180)
            # Regenerar las cajas
            cajas = crear_cajas(caja_texturas, 3)
        elif piezasMapa == 2:
            fondo = Fondo(texturas["scene3"].archivo)
            personaje.teletransportar(-anchopantalla + 100, 180)
            # Regenerar las cajas
            cajas = crear_cajas(caja_texturas, 3)
        elif piezasMapa == 3:
            fondo = Fondo(texturas["scene4"].archivo)
            personaje.teletransportar(-anchopantalla + 100, 180)
            # Regenerar las cajas
            cajas = crear_cajas(caja_texturas, 3)
        fondo.cargarTextura()


class Princesa:
    def __init__(self, x, y, factor_x, factor_y, lado, texturas_idle):
        self.x = x
        self.y = y
        self.factor_x = factor_x
        self.factor_y = factor_y
        self.lado = lado
        self.texturas_idle = texturas_idle
        self.frame = 0
        self.frame_rate = 0  # Change frame every 5 updates
        self.frame_counter = 0
        self.direccion = -1
        self.estado = "idle"  # "idle" or "walking"

    def dibujar(self):
        # Habilitar texturas
        glEnable(GL_TEXTURE_2D)

        # Aplicar la textura correcta según el estado
        if self.estado == "idle":
            self.texturas_idle[self.frame % len(self.texturas_idle)].aplicarTextura()

        # Impresión de depuración
        # print(f"Estado: {self.estado}, Frame: {self.frame}")

        # Aplicar la escala para el flip
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glScalef(self.direccion, 1, 1)  # Flip the sprite based on direction
        glTranslatef(-self.x, -self.y, 0)

        # Dibujar el personaje como un cuadrado
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.x - self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x + self.lado / self.factor_x, self.y - self.lado / self.factor_y)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x - self.lado / self.factor_x, self.y + self.lado / self.factor_y)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def idle(self):
        self.frame_rate = 28
        self.estado = "idle"
        self.actualizar_animacion()

    def actualizar_animacion(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            if self.estado == "idle":
                self.frame = (self.frame + 1) % len(self.texturas_idle)
            self.frame_counter = 0


def crear_cajas(caja_texturas, cantidad):
    cajas = []
    # Asegurarse de que haya al menos dos cajas trampa y una no trampa
    trampa_indices = random.sample(range(cantidad), 2)
    no_trampa_indices = [i for i in range(cantidad) if i not in trampa_indices]

    for i in range(cantidad):
        x = random.randint(-anchopantalla // 2 + 100, anchopantalla // 2 + 100)
        if i in trampa_indices:
            trampa = True
        else:
            trampa = False
        caja = CajaRompible(x, 110, 2, 2, 90, caja_texturas, "saludable", trampa)
        cajas.append(caja)
    return cajas


def render_text(text, font, text_color, bg_color):
    text_surface = font.render(text, True, text_color, bg_color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id, width, height


def draw_text(texture_id, width, height, x, y, bg_color):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor3f(bg_color[0], bg_color[1], bg_color[2])
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)  # Reset color to white for text
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(x, y)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(x + width, y)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(x + width, y + height)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(x, y + height)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def game_over_screen():
    global game_over  # Asegúrate de que estás usando la variable global
    print("Game Over")

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Fondo de pantalla
    fondo_game_over = Fondo(texturas["game_over"].archivo)  # Access the archivo attribute
    fondo_game_over.cargarTextura()
    fondo_game_over.dibujarFondo()  # Dibuja el fondo de Game Over

    # Mostrar el texto de game over
    game_over_text = "Game Over"
    text_color = (255, 0, 0)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(game_over_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, height // 2, bg_color)

    # Mostrar el texto para las opciones
    reset_text = "Presiona 'R' para reiniciar"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(reset_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, -height // 2 - 50, bg_color)

    quit_text = "Presiona 'Q o ESC' para salir"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(quit_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, -height // 2 - 150, bg_color)
    glFlush()

    audio_powerup_song.stop()
    audio_night_shade.play()
    # Esperar a que el jugador presione una tecla
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reiniciar_juego()  # Reiniciar el juego
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  # Actualizar la pantalla para mostrar el Game Over
        pygame.time.wait(100)  # Esperar un poco antes de volver a dibujar


def reiniciar_juego():
    # Relanzar el programa entero
    os.execl(sys.executable, sys.executable, *sys.argv)


def pantalla_inicio():
    global inicio
    print("Pantalla de inicio")

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Fondo de pantalla
    fondo_inicio = Fondo(texturas["scene1"].archivo)  # Access the archivo attribute
    fondo_inicio.cargarTextura()
    fondo_inicio.dibujarFondo()  # Dibuja el fondo de inicio

    # Mostrar el texto de inicio
    inicio_text = "Bienvenid@ a TerraTec - Ayuda a Alaric a encontrar a la princesa Elowen"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(inicio_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, height // 2, bg_color)

    # Mostrar el texto para las opciones
    start_text = "Presiona 'S' para comenzar"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(start_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, -height // 2 - 50, bg_color)

    quit_text = "Presiona 'Q o ESC' para salir"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(quit_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, -height // 2 - 150, bg_color)
    glFlush()

    # Esperar a que el jugador presione una tecla
    while inicio:
        for _ in pygame.event.get():
            if _.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif _.type == pygame.KEYDOWN:
                if _.key == pygame.K_s:
                    inicio = False  # Salir de la pantalla de inicio
                    # Iniciar la cancion de powerup
                    audio_powerup_song.play()
                elif _.key == pygame.K_q or _.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  # Actualizar la pantalla para mostrar


def pantalla_ganar():
    global ganar

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Fondo de pantalla
    fondo_ganar = Fondo(texturas["scene5"].archivo)  # Access the archivo attribute
    fondo_ganar.cargarTextura()
    fondo_ganar.dibujarFondo()  # Dibuja el fondo de inicio

    # Mostrar el texto de ganar
    ganar_text = "Gracias a tu extensa búsqueda, has encontrado todas las piezas del mapa y has podido dar conmigo"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(ganar_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, height // 2, bg_color)

    # Dibujar a la princesa
    texturas_princesa_idle = [texturas["princess_idle1"], texturas["princess_idle2"], texturas["princess_idle3"],
                              texturas["princess_idle4"], texturas["princess_idle5"], texturas["princess_idle6"],
                              texturas["princess_idle7"]]

    princesa = Princesa(-anchopantalla // 2 + anchopantalla/2, 280, 1.3, 0.975, 200, texturas_princesa_idle)

    # Mostrar el texto para las opciones
    reset_text = "Presiona 'R' para reiniciar"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(reset_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, -height // 2 - 50, bg_color)

    quit_text = "Presiona 'Q o ESC' para salir"
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(quit_text, font, text_color, bg_color)
    draw_text(texture_id, width, height, -width // 2, -height // 2 - 150, bg_color)

    glTranslatef(0, -altopantalla + 25, 0)
    espaciado_bloques = 50
    cantidad_bloques = 80

    # Seleccionar una textura
    textura_bloque = texturas["dirt1"]

    dirt = Bloque(espaciado_bloques, textura_bloque)  # Use the selected texture instance

    for x in range(cantidad_bloques):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 25 + espaciado_bloques * x, 0, 0)
        dirt.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    textura_bloque = texturas["dirt_grass1"]
    grass = Bloque(espaciado_bloques, textura_bloque)

    for x in range(cantidad_bloques):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 25 + espaciado_bloques * x, 50, 0)
        grass.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    glPushMatrix()
    glTranslatef(2300, -40, 0)
    glScalef(1.5, 1.5, 1)
    personaje.dibujar()
    glPopMatrix()

    glPushMatrix()
    princesa.dibujar()
    glPopMatrix()
    glFlush()

    audio_powerup_song.stop()
    audio_night_shade.play()

    # Esperar a que el jugador presione una tecla
    while ganar:
        for _ in pygame.event.get():
            if _.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif _.type == pygame.KEYDOWN:
                if _.key == pygame.K_r:
                    print("Reiniciar")
                    reiniciar_juego()
                elif _.key == pygame.K_q or _.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()  # Actualizar la pantalla para mostrar

def mostrar():
    global piezasMapa
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Dibujar el fondo
    fondo.dibujarFondo()

    glTranslatef(0, -altopantalla + 25, 0)

    # Mostrar vidas restantes
    vidas_texto = f'Vidas: {personaje.vidas}'
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(vidas_texto, font, text_color, bg_color)
    draw_text(texture_id, width, height, -anchopantalla + 10, altopantalla + 800, bg_color)

    # Mostrar piezas de mapa encontradas
    piezas_texto = f'Piezas de mapa: {piezasMapa}'
    text_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    texture_id, width, height = render_text(piezas_texto, font, text_color, bg_color)
    draw_text(texture_id, width, height, -anchopantalla + 10, altopantalla + 700, bg_color)

    espaciado_bloques = 150

    if piezasMapa >= 1:
        textura_mapa = texturas["mapa_1"]
        mapa1 = Bloque(150, textura_mapa)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 100 + espaciado_bloques, altopantalla + 500, 0)
        mapa1.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
    if piezasMapa >= 2:
        textura_mapa = texturas["mapa_2"]
        mapa2 = Bloque(150, textura_mapa)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 200 + espaciado_bloques, altopantalla + 500, 0)
        mapa2.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
    if piezasMapa >= 3:
        textura_mapa = texturas["mapa_3"]
        mapa3 = Bloque(150, textura_mapa)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 300 + espaciado_bloques, altopantalla + 500, 0)
        mapa3.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
    if piezasMapa >= 4:
        textura_mapa = texturas["mapa_4"]
        mapa4 = Bloque(150, textura_mapa)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 400 + espaciado_bloques, altopantalla + 500, 0)
        mapa4.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    espaciado_bloques = 50
    cantidad_bloques = 80

    # Seleccionar una textura
    textura_bloque = texturas["dirt1"]

    dirt = Bloque(espaciado_bloques, textura_bloque)  # Use the selected texture instance

    for x in range(cantidad_bloques):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 25 + espaciado_bloques * x, 0, 0)
        dirt.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    textura_bloque = texturas["dirt_grass1"]
    grass = Bloque(espaciado_bloques, textura_bloque)

    for x in range(cantidad_bloques):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 25 + espaciado_bloques * x, 50, 0)
        grass.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    # Actualizar la posición del personaje
    personaje.actualizar(gravedad)

    glPushMatrix()
    personaje.dibujar()
    glPopMatrix()

    # Dibujar la caja rompible
    glPushMatrix()
    for caja in cajas:
        caja.dibujar()
    glPopMatrix()

    glFlush()


def inicializacion():
    glClearColor(grisClaro.get_r(), grisClaro.get_g(), grisClaro.get_b(), 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Asegúrate de cargar la identidad
    # Ajustar la proyección ortográfica para que la cámara esté por encima del eje Y negativo
    gluOrtho2D(-anchopantalla, anchopantalla, -altopantalla, altopantalla)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    font = pygame.font.SysFont('Arial', 64)
    audio_hurt = pygame.mixer.Sound("./audio/player_hurt.mp3")
    audio_map_pickup = pygame.mixer.Sound("./audio/map_pickup.mp3")
    audio_powerup_song = pygame.mixer.Sound("./audio/powerup.mp3")
    audio_night_shade = pygame.mixer.Sound("./audio/night_shade.mp3")

    display = (anchopantalla, altopantalla)
    pygame.display.set_mode(display, pygame.WINDOWMAXIMIZED | OPENGL)  # Sin la opción RESIZABLE

    for key, value in texturas.items():
        textura = Textura(value)
        textura.cargarTextura()
        texturas[key] = textura

    fondo = Fondo(texturas["scene1"].archivo)
    fondo.cargarTextura()

    caballero_caminando = [texturas["knight_walk1"], texturas["knight_walk2"], texturas["knight_walk3"],
                           texturas["knight_walk4"], texturas["knight_walk5"], texturas["knight_walk6"],
                           texturas["knight_walk7"], texturas["knight_walk8"]]
    caballero_idle = [texturas["knight_idle1"], texturas["knight_idle2"], texturas["knight_idle3"],
                      texturas["knight_idle4"]]
    caballero_corriendo = [texturas["knight_run1"], texturas["knight_run2"], texturas["knight_run3"],
                           texturas["knight_run4"], texturas["knight_run5"], texturas["knight_run6"],
                           texturas["knight_run7"]]
    caballero_hurt = [texturas["knight_hurt1"], texturas["knight_hurt2"]]
    caballero_atacando = [texturas["knight_attack1"], texturas["knight_attack2"], texturas["knight_attack3"],
                          texturas["knight_attack4"], texturas["knight_attack5"]]

    personaje = Personaje(-anchopantalla + 100, 180, 2, 1.875, 200, caballero_caminando, caballero_idle,
                          caballero_corriendo, caballero_hurt, caballero_atacando, 3)

    caja_texturas = [texturas["caja_1"], texturas["caja_2"]]
    cajas = crear_cajas(caja_texturas, 3)

    inicializacion()

    gravedad = 1
    fuerza_salto = 20

    game_over = False
    ganar = False
    inicio = True

    pantalla_inicio()  # Call the start screen function

    try:
        while True:
            if personaje.vidas == 0:
                game_over = True
                game_over_screen()
            elif piezasMapa == 4:
                ganar = True
                pantalla_ganar()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in keys:
                            keys[event.key] = True
                        if event.key == pygame.K_SPACE:
                            personaje.saltar(fuerza_salto)
                    elif event.type == pygame.KEYUP:
                        if event.key in keys:
                            keys[event.key] = False
                    elif event.type == pygame.VIDEORESIZE:
                        anchopantalla, altopantalla = event.w, event.h
                        pygame.display.set_mode((anchopantalla, altopantalla), OPENGL | pygame.RESIZABLE)
                        inicializacion()

                if keys[pygame.K_a] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    personaje.correr_izquierda()
                elif keys[pygame.K_d] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    personaje.correr_derecha()
                elif keys[pygame.K_a]:
                    personaje.mover_izquierda()
                elif keys[pygame.K_d]:
                    personaje.mover_derecha()
                elif keys[pygame.K_u]:
                    personaje.atacar(cajas)
                elif keys[pygame.K_SPACE]:
                    personaje.saltar(fuerza_salto)
                else:
                    personaje.idle()

                personaje.actualizar_animacion()

                mostrar()
                pygame.display.flip()
                pygame.time.wait(10)

    except KeyboardInterrupt:
        pygame.quit()
        quit()