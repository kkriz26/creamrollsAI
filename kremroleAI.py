import math
import os
import random
from collections import namedtuple
from enum import Enum
from time import sleep

import numpy as np
import pygame
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
                           QUIT, RLEACCEL)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
newfactor = 1
Point = namedtuple('Point', 'x, y')
enemies = pygame.sprite.Group()
treadmills = pygame.sprite.Group()
counter = 0
record = 0
reward = 0
done = False

class Direction(Enum):
    RIGHT = 4
    LEFT = 3
    UP = 1
    DOWN = 2



class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.image.load(os.path.abspath("mike.png")).convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.reset()


	def reset(self):
		self.surf = pygame.image.load(os.path.abspath("mike.png")).convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect()
		self.rect.y = 100
		self.rect.x = 200
		for enemy in enemies:
			enemy.kill()
		for treadmill in treadmills:
			treadmill.kill()

	#def update(self, pressed_keys, action):
	def update(self, action):

		if np.array_equal(action, [1, 0, 0, 0, 0]):# or pressed_keys[K_UP]:
			self.rect.move_ip(0, -50)
		if np.array_equal(action, [0, 1, 0, 0, 0]):# or pressed_keys[K_DOWN]: #down
			self.rect.move_ip(0, 50)
		if np.array_equal(action, [0, 0, 1, 0, 0]):# or  pressed_keys[K_LEFT]: # left
			self.rect.move_ip(-50, 0)
		if np.array_equal(action, [0, 0, 0, 1, 0]):# or pressed_keys[K_RIGHT]: #right
			self.rect.move_ip(50, 0)
		if np.array_equal(action, [0, 0, 0, 0, 1]):# or pressed_keys[K_RIGHT]: #right
			pass

		

		global reward
		if self.rect.left < 0:
			self.rect.left = 0
			#reward -= 20
			#self.reset()
			#update_BMI(restart=False)
			#update_counter(restart=False)
			#player.reset()


		if self.rect.right > SCREEN_WIDTH:
			self.rect.right = SCREEN_WIDTH
			#reward -= 20
			#self.reset()
			#update_BMI(restart=False)
			#update_counter(restart=False)
			#player.reset()

		if self.rect.top <= 0:
			self.rect.top = 0
			#reward -= 20
			#self.reset()
			#update_BMI(restart=False)
			#update_counter(restart=False)
			#player.reset()

		if self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT
			#reward -= 20
			#self.reset()
			#update_BMI(restart=False)
			#update_counter(restart=False)
			#player.reset()


	def update_size(self):
		pass
"""		newfactor = BMI - 22
		newsize1 = newfactor*3 + 51
		newsize2 = newfactor*3 + 62
		self.surf = pygame.transform.scale(self.surf, (newsize1, newsize2))
##		self.rect = self.surf.get_rect()
		self.rect = self.rect.inflate(newfactor, newfactor)
##self.rect.inflate = (newfactor,  newfactor)
"""#turned off for AI game, to make it simpler
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surf = pygame.image.load(os.path.abspath("kremrole.png")).convert_alpha()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(SCREEN_WIDTH,
				random.randint(0, SCREEN_HEIGHT)
			)
		)
		self.speed = 10#random.randint(5, 10)
	
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()
			global reward
			global counter
			#reward += 1
			dice = random.randint(0, 9)
			txt = font.render(str(textbark[dice]), True, (0, 255, 0), (0, 0, 128))
			txtrct= txt.get_rect()
			txtrct.center = (300, 300)
			screen.blit(txt, txtrct)
			#sleep(0.5)

class Treadmill(pygame.sprite.Sprite):
	def __init__(self):
		super(Treadmill, self).__init__()
		self.surf = pygame.image.load(os.path.abspath("TREADMILL.png")).convert_alpha()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(SCREEN_WIDTH,
				random.randint(0, SCREEN_HEIGHT)
			)
		)
		self.speed = 10#random.randint(5, 10)
	
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()
			#sleep(0.5)

pygame.mixer.init()

pygame.init()
pygame.display.set_caption("Mickeys`s Creamroll Nightmare")
pygame.mixer.init()
clock = pygame.time.Clock()


pygame.time.set_timer(pygame.USEREVENT, 1000)




pygame.mixer.music.load(os.path.abspath("Mortal_Kombat.mp3")) #bugs off in agent controlled game
EXPLOSION = pygame.mixer.Sound('BOOM.wav')
pygame.mixer.music.play(loops=-1)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 375)

player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
playergroup = pygame.sprite.Group()
playergroup.add(player) 

#boom = pygame.mixer.Sound(os.path.abspath("BOOM.wav"))
#boom = pygame.mixer.Sound("Collision.ogg")
BMI = 23
font = pygame.font.Font('freesansbold.ttf', 32)
textBMI = font.render('BMI=', True, (0, 255, 0), (0, 0, 128))
textBMIRect = textBMI.get_rect()
textBMIRect.center = (40, 560)
textBMI2 = font.render(str(BMI), True, (0, 255, 0), (0, 0, 128))
textRectBMI2 = textBMI2.get_rect()
textRectBMI2.center = (120, 560)

textcounter = font.render(str(counter), True, (0, 255, 0), (0, 0, 128))
textRect4 = textcounter.get_rect()
textRect4.center = (760, 560)

text3 = font.render("You are too fat to get out the door", True, (0, 255, 0), (0, 0, 128))
textRect3 = text3.get_rect()
textRect3.center = (300, 300)
scoretext = font.render("You have survived " + str(counter) + " seconds", True, (0, 255, 0), (0, 0, 128))
scorerect = scoretext.get_rect()
scorerect.center = (300, 250)

textbark = ["Great!", "You Rock!", "Finish Him!","Yeaa!", "Destroy Whats Left of Him!", "Splendid", "Left Hook!", "Right Punch!", "You got it!", "Cool!"]
textbarklose = ["You Suck!", "Game Over!", "Omae wa mou shinde iru!", "You Fool!", "Better Luck Next Time!", "Obliterated!", "It Ends Now...", "Goodbye, Mr. Anderson", "Goodnight", "RIP!"]
highestscore = font.render('Record', True, (0, 255, 0), (0, 0, 128))
highestscoreRect = highestscore.get_rect()
highestscoreRect.center = (60, 40)
highestscore2 = font.render(str(record), True, (0, 255, 0), (0, 0, 128))
highestscoreRect2 = highestscore2.get_rect()
highestscoreRect2.center = (140, 40)

def update_BMI(restart=False, treadmill=False):
	global BMI
	global reward
	global done
	if restart == False and treadmill == False:
		BMI += 3
		reward -= 10
		done = False
	if restart == True:
		done = True
		BMI = 23
	if treadmill == True:
		done = False
		reward += 100
		BMI -= 3
	player.update_size()
	return reward, done


def update_counter(restart=False):
	global counter
	global record
	global reward
	global done
	if restart == False:
		counter += 1
		done = False
		#some more alternative rewarding
		'''if counter == 10:
			reward += 1
		if counter == 20:
			reward += 4
		if counter == 30:
			reward += 5
		if counter > 40:
			reward += 1'''
	else:
		done = True

	return reward, done

def wipe_score():
	global done
	global reward
	global counter
	global record
	if counter > record:
		record = counter
	done = False
	counter = 0
	reward = 0
		
running = True
#while running: #turned off for AI controlled game
def playstep(action):
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False
		elif event.type == ADDENEMY:
			dice = random.randint(1, 4)

			if dice == 10:
				new_treadmill = Treadmill()
				treadmills.add(new_treadmill)
				all_sprites.add(new_treadmill)
			elif len(enemies) <1:
				new_enemy = Enemy()
				enemies.add(new_enemy)
				all_sprites.add(new_enemy)

		if event.type == pygame.USEREVENT: 
			update_counter()



	#pressed_keys = pygame.key.get_pressed()
	#player.update(pressed_keys, [10, 10, 10, 10])
	player.update(action)
	enemies.update()
	treadmills.update()
	screen.fill((0, 0, 0))
	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)


	textBMI2 = font.render(str(BMI), True, (0, 255, 0), (0, 0, 128))	
	screen.blit(textBMI, textBMIRect)
	screen.blit(textBMI2, textRectBMI2)
	textcounter = font.render(str(counter), True, (0, 255, 0), (0, 0, 128))
	screen.blit(textcounter, textRect4)
	highestscore2 = font.render(str(record), True, (0, 255, 0), (0, 0, 128))
	screen.blit(highestscore, highestscoreRect)
	screen.blit(highestscore2, highestscoreRect2)
	player_rect = player.rect
	#alternative rewarding to use along with a penalty with hit usually not needed
	'''for sprite in enemies:
		global reward
		if math.sqrt((player_rect.top -sprite.rect.bottom)**2) < 51 and player_rect.top > sprite.rect.bottom and (player_rect.right in range(sprite.rect.left -20, sprite.rect.right) or player_rect.left in range(sprite.rect.left, sprite.rect.right)  ):
			reward += 0.3
		if math.sqrt((player_rect.right -sprite.rect.left)**2) < 61 and player_rect.right < sprite.rect.left and (sprite.rect.top in range(player_rect.top, player_rect.bottom) or sprite.rect.bottom in range(player_rect.top, player_rect.bottom)):
			reward -= 0.1
		if math.sqrt((player_rect.bottom -sprite.rect.top)**2) < 51 and player_rect.bottom < sprite.rect.top and (player_rect.right in range(sprite.rect.left -20, sprite.rect.right) or player_rect.left in range(sprite.rect.left, sprite.rect.right) ):
			reward += 0.3
		if math.sqrt((player_rect.left -sprite.rect.right)**2) < 51 and player_rect.left > sprite.rect.right and (sprite.rect.top in range(player_rect.top, player_rect.bottom) or sprite.rect.bottom in range(player_rect.top, player_rect.bottom)):
			reward += 0.3'''
	if pygame.sprite.groupcollide(playergroup, enemies, False, True):
		update_BMI()
		textBMI2 = font.render(str(BMI), True, (0, 255, 0), (0, 0, 128))

		scoretext = font.render("You have survived " + str(counter) + " seconds", True, (0, 255, 0), (0, 0, 128))
		scorerect = scoretext.get_rect()
		scorerect.center = (300, 250)
	if pygame.sprite.groupcollide(playergroup, treadmills, False, True):
		update_BMI(treadmill=True)
		textBMI2 = font.render(str(BMI), True, (0, 255, 0), (0, 0, 128))

	if BMI > 23:
		update_BMI(True)
		update_counter(True)
		player.reset()
		#EXPLOSION.play()
		dice = random.randint(0, 9)
		txt = font.render(str(textbarklose[dice]), True, (0, 255, 0), (0, 0, 128))
		txtrct = txt.get_rect()
		txtrct.center = (300, 300)
		screen.blit(txt, txtrct)
		#sleep(0.5)
		
		#screen.blit(scoretext, scorerect)
		#running = False

	
#		boom.play()
#		running = False

	#(reward, counter, done)
	pygame.display.flip()
	clock.tick(120)

pygame.mixer.music.stop()
pygame.mixer.quit()
