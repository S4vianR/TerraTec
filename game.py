import pygame
from PyOpenGLtoolbox import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Dimensiones de la pantalla
anchopantalla = 1920
altopantalla = 1080

# Textura seleccionada
textura_seleccionada = ""

keys = {
    pygame.K_w: False,
    pygame.K_s: False,
    pygame.K_a: False,
    pygame.K_d: False,
    pygame.K_SPACE: False,
    pygame.K_LSHIFT: False,
    pygame.K_RSHIFT: False
}

# Base del piso
base_piso = 155

# Grupos para los objetos
grupo_bloques = {
    "dirt": [],
    "grass": [],
}


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

            self.textura = pygame.image.tostring(imagen, "RGBA", 1)
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
    "dirt1": "./textures/dirt1.png",
    "dirt2": "./textures/dirt2.png",
    "dirt_grass1": "./textures/dirt_grass1.png",
    "dirt_grass2": "./textures/dirt_grass2.png",
    "grass1": "./textures/grass1.png",
    "grass2": "./textures/grass2.png",
    "forest_background": "./textures/forest_background.jpeg",
    "pink_monster": "./textures/Pink_Monster/Pink_Monster.png",
    "walk1": "./textures/Pink_Monster/Walk/Walk1.png",
    "walk2": "./textures/Pink_Monster/Walk/Walk2.png",
    "walk3": "./textures/Pink_Monster/Walk/Walk3.png",
    "walk4": "./textures/Pink_Monster/Walk/Walk4.png",
    "walk5": "./textures/Pink_Monster/Walk/Walk5.png",
    "walk6": "./textures/Pink_Monster/Walk/Walk6.png",
    "idle1": "./textures/Pink_Monster/Idle/Idle1.png",
    "idle2": "./textures/Pink_Monster/Idle/Idle2.png",
    "idle3": "./textures/Pink_Monster/Idle/Idle3.png",
    "idle4": "./textures/Pink_Monster/Idle/Idle4.png",
    "run1":  "./textures/Pink_Monster/Run/Run1.png",
    "run2":  "./textures/Pink_Monster/Run/Run2.png",
    "run3":  "./textures/Pink_Monster/Run/Run3.png",
    "run4":  "./textures/Pink_Monster/Run/Run4.png",
    "run5":  "./textures/Pink_Monster/Run/Run5.png",
    "run6":  "./textures/Pink_Monster/Run/Run6.png",
}


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

            self.textura = pygame.image.tostring(imagen, "RGBA", 1)
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
    def __init__(self, x, y, lado, texturas_caminando, texturas_idle, texturas_corriendo):
        self.x = x
        self.y = y
        self.lado = lado
        self.texturas_caminando = texturas_caminando
        self.texturas_idle = texturas_idle
        self.texturas_corriendo = texturas_corriendo
        self.vel_y = 0
        self.en_el_aire = False
        self.direccion = 1  # 1 for right, -1 for left
        self.frame = 0
        self.frame_rate = 0  # Change frame every 5 updates
        self.frame_counter = 0
        self.velocidad_movimiento = 0
        self.estado = "idle"  # "idle" or "walking"

    def dibujar(self):
        # Habilitar texturas
        glEnable(GL_TEXTURE_2D)

        # Aplicar la textura correcta según el estado
        if self.estado == "walking":
            self.texturas_caminando[self.frame].aplicarTextura()
        elif self.estado == "idle":
            self.texturas_idle[self.frame].aplicarTextura()
        elif self.estado == "running":
            self.texturas_corriendo[self.frame].aplicarTextura()

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
        glVertex2f(self.x - self.lado / 2, self.y - self.lado / 1.25)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x + self.lado / 2, self.y - self.lado / 1.25)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.lado / 2, self.y + self.lado / 1.25)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x - self.lado / 2, self.y + self.lado / 1.25)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

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
        self.frame_rate = 45
        self.estado = "idle"
        self.actualizar_animacion()

    def saltar(self, fuerza):
        if not self.en_el_aire:
            self.vel_y = fuerza
            self.en_el_aire = True

    def actualizar(self, gravedad):
        if self.en_el_aire:
            self.y += self.vel_y
            self.vel_y -= gravedad
            if self.y <= base_piso:
                self.y = base_piso
                self.en_el_aire = False
                self.vel_y = 0

    def actualizar_animacion(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            if self.estado == "walking":
                self.frame = (self.frame + 1) % len(self.texturas_caminando)
            elif self.estado == "idle":
                self.frame = (self.frame + 1) % len(self.texturas_idle)
            elif self.estado == "running":
                self.frame = (self.frame + 1) % len(self.texturas_corriendo)
            self.frame_counter = 0


def drawLine(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def planoCartesiano():
    glPushMatrix()

    # Eje X
    drawLine(-anchopantalla, 0, anchopantalla, 0)

    # Eje Y
    drawLine(0, -altopantalla, 0, altopantalla)

    glPopMatrix()


def mostrar():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Dibujar el fondo
    fondo.dibujarFondo()

    glTranslatef(0, -altopantalla + 25, 0)

    espaciadoBloques = 50
    cantidad_bloques= 80

    # Seleccionar una textura
    textura_seleccionada = texturas["dirt1"]

    dirt = Bloque(espaciadoBloques, textura_seleccionada)  # Use the selected texture instance

    for x in range(cantidad_bloques):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 25 + espaciadoBloques * x, 0, 0)
        dirt.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    textura_seleccionada = texturas["dirt_grass1"]
    grass = Bloque(espaciadoBloques, textura_seleccionada)

    for x in range(cantidad_bloques):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glTranslatef(-anchopantalla + 25 + espaciadoBloques * x, 50, 0)
        grass.dibujarBloque()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    # Actualizar la posición del personaje
    personaje.actualizar(gravedad)

    glPushMatrix()
    personaje.dibujar()
    glPopMatrix()

    glFlush()


def inicializacion():
    glClearColor(grisClaro.get_r(), grisClaro.get_g(), grisClaro.get_b(), 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Asegúrate de cargar la identidad
    # Ajustar la proyección ortográfica para que la cámara esté por encima del eje Y negativo
    gluOrtho2D(-anchopantalla, anchopantalla, -altopantalla, altopantalla)


if __name__ == '__main__':
    glutInit()  # Initialize GLUT
    pygame.init()

    # Cambia esta línea para permitir que la ventana sea redimensionable
    display = (anchopantalla, altopantalla)
    pygame.display.set_mode(display, OPENGL | pygame.RESIZABLE)

    # Cargar texturas del diccionario
    for key, value in texturas.items():
        textura = Textura(value)
        textura.cargarTextura()
        texturas[key] = textura

    # Cargar la textura de fondo
    fondo = Fondo("./textures/forest_background.jpeg")
    fondo.cargarTextura()

    # Lista de texturas para la animación de caminar
    texturas_caminando = [texturas["walk1"], texturas["walk2"], texturas["walk3"], texturas["walk4"]]

    # Lista de texturas para la animación de idle
    texturas_idle = [texturas["idle1"], texturas["idle2"], texturas["idle3"], texturas["idle4"]]

    # Lista de texturas para la animación de correr
    texturas_corriendo = [texturas["run1"], texturas["run2"], texturas["run3"], texturas["run4"], texturas["run5"],
                          texturas["run5"]]

    personaje = Personaje(0, base_piso, 100, texturas_caminando, texturas_idle, texturas_corriendo)

    inicializacion()

    gravedad = 1  # Gravity value
    fuerza_salto = 20  # Jump force

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in keys:
                        keys[event.key] = True
                    if event.key == pygame.K_SPACE:  # Press SPACE to jump
                        personaje.saltar(fuerza_salto)
                elif event.type == pygame.KEYUP:
                    if event.key in keys:
                        keys[event.key] = False
                elif event.type == pygame.VIDEORESIZE:
                    # Actualiza el tamaño de la ventana y la proyección
                    anchopantalla, altopantalla = event.w, event.h
                    pygame.display.set_mode((anchopantalla, altopantalla), OPENGL | pygame.RESIZABLE)
                    inicializacion()  # Reinitialize OpenGL settings

            if keys[pygame.K_a] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                personaje.correr_izquierda()
            elif keys[pygame.K_d] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                personaje.correr_derecha()
            elif keys[pygame.K_a]:
                personaje.mover_izquierda()
            elif keys[pygame.K_d]:
                personaje.mover_derecha()
            elif keys[pygame.K_SPACE]:
                personaje.saltar(fuerza_salto)
            else:
                personaje.idle()  # Cambiar a idle si no se está moviendo

            # Check if none of the movement keys are pressed
            if not any(keys.values()):
                personaje.idle()
            mostrar()
            pygame.display.flip()
            pygame.time.wait(10)

    except KeyboardInterrupt:
        pygame.quit()
        quit()
