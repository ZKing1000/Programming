import pygame, sys, math
from pygame.locals import *
from random import random
 
 
class Paddle():
  def __init__(self, screen, x, h):
    self.screen = screen
    (sw, sh) = screen.get_size()
    self.x = x - 25
    self.h = h
    self.y = sh / 2 - self.h / 2
    self.w = 50
    self.max_y = sh - h
    self.min_y = 0
    self.speed = 0
    self.score = 0
  def move(self, amount):
    self.speed = amount
    self.y = self.y + amount
    if self.y > self.max_y:
      self.y = self.max_y
    elif self.y < self.min_y:
      self.y = self.min_y
  def score_point(self):
    self.score += 1
  def draw(self):
    pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.w, self.h))
 
class Ball():
  def __init__(self, screen):
    self.screen = screen
    self.w = 50
    self.h = 50
    self.playclick = False
    self.reset()
  def reset(self):
    (sw, sh) = self.screen.get_size()
    self.x = sw / 2 - 25
    self.y = sh / 2 - 25
    angle = random() * math.radians(20)
    speed = 10
    self.dir_x = speed * math.cos(angle)
    self.dir_y = speed * math.sin(angle)
    if random() > 0.5:
      self.dir_x = -self.dir_x
    if random() > 0.5:
      self.dir_y = -self.dir_y
    self.timer = 2
  def update(self, time, p1, p2):
    if self.timer > 0:
      self.timer -= time
    else:
      self.x += self.dir_x
      self.y += self.dir_y
    (sw, sh) = self.screen.get_size()
    if self.x + 50 < 0:
      p2.score_point()
      self.reset()
    elif self.x > sw:
      p1.score_point()
      self.reset()
    else:
      if (self.y < 0 and self.dir_y < 0) or (self.y + self.h > sh and self.dir_y > 0):
        self.dir_y = - self.dir_y
        self.playclick = True
      selfrect = pygame.Rect(self.x, self.y, self.w, self.h)
      p1rect = pygame.Rect(p1.x, p1.y, p1.w, p1.h)
      p2rect = pygame.Rect(p2.x, p2.y, p2.w, p2.h)
      if selfrect.colliderect(p1rect) and self.dir_x < 0:
        self.dir_x = -self.dir_x
        self.dir_y += p1.speed
        self.playclick = True
      elif selfrect.colliderect(p2rect) and self.dir_x > 0:
        self.dir_x = -self.dir_x
        self.dir_y += p2.speed
        self.playclick = True
      if self.dir_y > 15:
        self.dir_y = 15
      elif self.dir_y < -15:
        self.dir_y = -15
  def draw(self, font, click):
    pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.w, self.h))
    if self.timer > 0:
      text = font.render("%.1f" % self.timer, True, (0, 0, 0))
      text_x = self.x - text.get_rect().width / 2 + 25
      text_y = self.y - text.get_rect().height / 2 + 25
      self.screen.blit(text, (text_x, text_y))
    if self.playclick:
      click.play()
      self.playclick = False
 
def main():
  pygame.init()
  pygame.mixer.init()
  click = pygame.mixer.Sound("click.wav");
  screen = pygame.display.set_mode((1000, 800))
  clock = pygame.time.Clock()
  pygame.font.init()
  p1 = Paddle(screen, 100, 150)
  p2 = Paddle(screen, 900, 150)
  ball = Ball(screen)
  font = pygame.font.SysFont(None, 50)
  while True:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
        sys.exit()
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    if keys[K_w] and not keys [K_s]:
      p1.move(-10)
    elif keys[K_s] and not keys[K_w]:
      p1.move(10)
    else:
      p1.move(0)
    # if keys[K_UP] and not keys [K_DOWN]:
      # p2.move(-10)
    # elif keys[K_DOWN] and not keys[K_UP]:
      # p2.move(10)
    # else:
      # p2.move(0)
    b_pos = ball.y + 25
    p2_pos = p2.y + 75
    if b_pos - p2_pos > 10:
      p2.move(10)
    elif p2_pos - b_pos > 10:
      p2.move(-10)
    else:
      p2.move(0)
    ball.update(1/60, p1, p2)
    p1.draw()
    p2.draw()
    ball.draw(font, click)
    text = font.render(str(p1.score) + " | " + str(p2.score), True, (255, 255, 255))
    text_x = 500 - text.get_rect().width / 2
    screen.blit(text, (text_x, 50))
    pygame.display.flip()
 
if __name__ == "__main__":
  main()
