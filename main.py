import pygame

#? Inicializar
pygame.init()
pantalla = pygame.display.set_mode((800,600))

#? clases
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
  
  

#? Configuraciones generales
icono = pygame.image.load('assets/favicon.svg')
background = pygame.image.load('assets/background.png')

pygame.display.set_caption('Invasion Espacial')
pygame.display.set_icon(icono)


#? Personaje
nave = Personaje('nave.png', 368, 500)


#? Inicializacion juego
run = True
while run:
  pantalla.blit(background, (0,0))

  #? Eventos
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        nave.movimiento = -1
      elif event.key == pygame.K_RIGHT:
        nave.movimiento = 1

    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        nave.movimiento = 0

    # ///////////////////////////
    if event.type == pygame.QUIT:
      run = False

  #? Movimiento
  nave.x += nave.movimiento
  if nave.x <= 0:
    nave.x = 0
  elif nave.x >= 736:
    nave.x = 736


  nave.show()
  pygame.display.update()
  