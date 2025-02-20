import math
import os
import random
from time import sleep

import pygame
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
                           QUIT, RLEACCEL)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
newfactor = 1

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.image.load(os.path.abspath("mike.png")).convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)

		self.rect = self.surf.get_rect()

	def update(self, pressed_keys):
		if pressed_keys[K_UP]:
			self.rect.move_ip(0, -5)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 5)
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-5, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(5, 0)


		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > SCREEN_WIDTH:
			self.rect.right = SCREEN_WIDTH
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT

	def update_size(self):
		newfactor = BMI - 22
		newsize1 = newfactor*3 + 51
		newsize2 = newfactor*3 + 62
		self.surf = pygame.transform.scale(self.surf, (newsize1, newsize2))
##		self.rect = self.surf.get_rect()
		self.rect = self.rect.inflate(newfactor, newfactor)
##self.rect.inflate = (newfactor,  newfactor)

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surf = pygame.image.load(os.path.abspath("kremrole.png")).convert_alpha()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(
				random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
				random.randint(0, SCREEN_HEIGHT),
			)
		)
		self.speed = random.randint(5, 20)
	
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()
	#	if pygame.sprite.spritecollideany(self, playergroup):
	#		updateBMI()
	#		self.kill()
			
			


pygame.mixer.init()

pygame.init()
pygame.display.set_caption("Mikys`s Kremrole Nightmare")
pygame.mixer.init()
clock = pygame.time.Clock()

counter = 0
pygame.time.set_timer(pygame.USEREVENT, 1000)




pygame.mixer.music.load(os.path.abspath("Mortal_Kombat.mp3"))
EXPLOSION = pygame.mixer.Sound('BOOM.wav')
pygame.mixer.music.play(loops=-1)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
playergroup = pygame.sprite.Group()
playergroup.add(player) 

#boom = pygame.mixer.Sound(os.path.abspath("BOOM.wav"))
#boom = pygame.mixer.Sound("Collision.ogg")
BMI = 23
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('BMI=', True, (0, 255, 0), (0, 0, 128))
textRect = text.get_rect()
textRect.center = (40, 560)
text2 = font.render(str(BMI), True, (0, 255, 0), (0, 0, 128))
textRect2 = text2.get_rect()
textRect2.center = (120, 560)

textcounter = font.render(str(counter), True, (0, 255, 0), (0, 0, 128))
textRect4 = textcounter.get_rect()
textRect4.center = (760, 560)

text3 = font.render("You are too fat to get out the door", True, (0, 255, 0), (0, 0, 128))
textRect3 = text3.get_rect()
textRect3.center = (300, 300)
scoretext = font.render("You have survived " + str(counter) + " seconds", True, (0, 255, 0), (0, 0, 128))
scorerect = scoretext.get_rect()
scorerect.center = (300, 250)

def update_BMI():
	global BMI
	BMI += 3
	player.update_size()
def update_counter():
	global counter
	counter += 1

running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False
		elif event.type == ADDENEMY:
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)
		if event.type == pygame.USEREVENT: 
			update_counter()



	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)
	enemies.update()
	screen.fill((0, 0, 0))
	if BMI > 50:

		screen.blit(text3, textRect3)
		screen.blit(scoretext, scorerect)

		player.kill()
		sleep(2)
		running = False
	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)
		


	screen.blit(text, textRect)
	screen.blit(text2, textRect2)
	textcounter = font.render(str(counter), True, (0, 255, 0), (0, 0, 128))
	screen.blit(textcounter, textRect4)

	if pygame.sprite.groupcollide(playergroup, enemies, False, True):
#		player.kill()
		update_BMI()
		text2 = font.render(str(BMI), True, (0, 255, 0), (0, 0, 128))

		screen.blit(text2, textRect2)
#		update()
		scoretext = font.render("You have survived " + str(counter) + " seconds", True, (0, 255, 0), (0, 0, 128))
		scorerect = scoretext.get_rect()
		scorerect.center = (300, 250)
##		textRect4 = textcounter.get_rect()
##		screen.blit(textcounter, textRect4)
	if BMI > 50:

		textcounter = font.render(str(counter), True, (0, 255, 0), (0, 0, 128))
		textRect4 = textcounter.get_rect()
		textRect4.center = (760, 560)
		EXPLOSION.play()
		screen.blit(text3, textRect3)
		screen.blit(scoretext, scorerect)


	
#		boom.play()
#		running = False
	pygame.display.flip()
	clock.tick(30)
	if BMI > 50:
		pygame.time.wait(3000)
		running = False
		player.kill()		

pygame.mixer.music.stop()
pygame.mixer.quit()
