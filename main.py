import pygame
from pygame import mixer
import random, math
import io

#? Inicializar
pygame.init()
pantalla = pygame.display.set_mode((800,600))

#? clases y funciones
class Personaje():
  movimiento = 0

  def __init__(self, image, x, y):
    self.image = f'assets/{image}'
    self.x = x
    self.y = y
  
  def set_image(self):
    return pygame.image.load(self.image)
  
  def show(self):
    pantalla.blit(self.set_image(), (self.x, self.y))
  
class Enemigo(Personaje):
  movimiento = (2,.1) if random.randint(1,2) == 1 else (-2,.1)

  def __init__(self, image, x, y):
    self.image = f'assets/{image}'
    self.x = random.randint(0,736)
    self.y = random.randint(100, 290)

  def reaparecer(self):
    self.x = random.randint(0,736)
    self.y = random.randint(100, 270)

class Bala(Personaje):
  movimiento = 8
  visible = False
  disparo = mixer.Sound('assets/sound/disparo.mp3')
  disparo.set_volume(0.03)
  impacto = mixer.Sound('assets/sound/Golpe.mp3')
  impacto.set_volume(0.03)


  def show(self, x_jugador):
    self.visible = True
    pantalla.blit(self.set_image(), (x_jugador, self.y))


def colision(x1,x2,y1,y2):
  distancia = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
  return True if distancia < 30 else False

def texto(x,y, texto):
  texto = font.render(texto, True, (255,255,255))
  pantalla.blit(texto,(x,y))

def font_bytes(font):
  with open(font, 'rb') as f:
    ttf_bytes = f.read()
  return io.BytesIO(ttf_bytes)

#? Variables generales
puntaje = 0
alive = True
aliens = []
numero_aliens = 8

#? Configuraciones generales
icono = pygame.image.load('assets/favicon.svg')
background = pygame.image.load('assets/background.png')
mixer.music.load('assets/sound/soundtrack.mp3')
font_byte = font_bytes('assets/font/8-bit-hud.ttf')
font = pygame.font.Font(font_byte, 18)


pygame.display.set_caption('Invasion Espacial')
pygame.display.set_icon(icono)
mixer.music.set_volume(0.05)
mixer.music.play(-1)


#? Personaje
nave = Personaje('nave.png', 368, 500)

#? Enemigo
for i in range(numero_aliens):
  alien = Enemigo('ovni.png', 0, 0)
  aliens.append(alien)

#? Bala
bala = Bala('bala.png', nave.x, nave.y)


#? Inicializacion juego
run = True
while run:
  pantalla.blit(background, (0,0))

  #? Eventos
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        nave.movimiento = -2.8
      elif event.key == pygame.K_RIGHT:
        nave.movimiento = 2.8
      elif event.key == pygame.K_SPACE:
        bala.disparo.play()
        if not bala.visible:
          bala.x = nave.x
          bala.show(nave.x + nave.movimiento)
        

    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        nave.movimiento = 0

    # ///////////////////////////
    if event.type == pygame.QUIT:
      run = False

  #? Movimiento Jugador
  nave.x += nave.movimiento
  if nave.x <= 0:
    nave.x = 0
  elif nave.x >= 736:
    nave.x = 736

  #? Movimiento Alien
  for alien in aliens:
    alien.show()
    alien.x += alien.movimiento[0]
    alien.y += alien.movimiento[1]
    if alien.x >= 736:
      alien.movimiento = (-2, .1)
    if alien.x <= 0:
      alien.movimiento = (2, .1)
    
    #? Detactar colision
    colision_ = colision(alien.x, bala.x, alien.y, bala.y)
    if colision_:
      bala.impacto.play()
      bala.y = 500
      bala.visible = False
      alien.reaparecer()
      puntaje += 1
    
    if alien.y > 400:
      for instancia in aliens:
        instancia.y = -1000
        instancia.movimiento = (0,0)
      alive = False
    

  #? Moviemiento Bala
  if bala.y <= -64:
    bala.y = 500
    bala.visible = False
  elif bala.visible:
    bala.show(bala.x)
    bala.y -= Bala.movimiento

  #? Detectar fin del juego
  if alive:
    texto(10,10, f'Puntaje: {puntaje}')
  else:
    texto(320,240, 'Perdiste')
    texto(302,270, f'Puntaje: {puntaje}')


  nave.show()
  pygame.display.update()