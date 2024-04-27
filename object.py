import pygame
import random


car_bluer = pygame.image.load("photos/bluer.png")
car_bluel = pygame.image.load("photos/bluel.png")

car_greenr = pygame.image.load("photos/greenr.png")
car_greenl = pygame.image.load("photos/greenl.png")

car_redr = pygame.image.load("photos/redr.png")
car_redl = pygame.image.load("photos/redl.png")

carsr = [car_bluer, car_greenr, car_redr]
carsl = [car_bluel, car_greenl, car_redl]

"""------------------------------------------------------------------------------------------------------------------
Parent class to all the objects of the game
"""


class Rectangle:

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def intersects(self, other):
		left = self.x
		top = self.y
		right = self.x + self.w
		bottom = self.y + self.h

		oleft = other.x
		otop = other.y
		oright = other.x + other.w
		obottom = other.y + other.h

		return not (left >= oright or right <= oleft or top >= obottom or bottom <= otop)


"""------------------------------------------------------------------------------------------------------------------
Frog class (kid of rectangle)
"""


class Frog(Rectangle):

	def __init__(self, x, y, w):
		super(Frog, self).__init__(x, y, w, w)
		self.image = pygame.image.load("photos/frog.png")
		self.attached = None

	def move(self, xdir, ydir, grid):
		self.x += xdir * grid   # (self.x + (xdir * grid)) // grid * grid
		self.y += ydir * grid

	def attach(self, log):
		self.attached = log

	def update(self, window_w, window_h):
		if self.attached is not None:
			self.x += self.attached.speed
		if self.x + self.w > window_w:
			self.x = window_w - self.w
		elif self.x < 0:
			self.x = 0
		if self.y + self.w > window_h:
			self.y = window_h - 1 * 68

	def draw(self, surface):
		surface.blit(self.image, (self.x, self.y))


"""------------------------------------------------------------------------------------------------------------------
Car class (kid of rectangle)
"""


class Car(Rectangle):

	def __init__(self, x, y, w, h, s):
		super(Car, self).__init__(x, y, w, h)
		if s > 0:

			self.image = carsr[random.randint(0, 2)]
		else:
			self.image = carsl[random.randint(0, 2)]
		self.speed = s

	def update(self, window_w):
		self.x += self.speed
		if self.speed > 0 and self.x > window_w + self.w:
			self.x = -self.w
		elif self.speed < 0 and self.x < -self.w:
			self.x = window_w

	def draw(self, surface):
		surface.blit(self.image, (self.x, self.y))


"""------------------------------------------------------------------------------------------------------------------
Log class (kid of rectangle)
"""


class Log(Rectangle):

	def __init__(self, x, y, w, h, s):
		super(Log, self).__init__(x, y, w, h)
		self.speed = s
		self.image = pygame.image.load("photos/log.png")

	def update(self, window_w):
		self.x += self.speed
		if self.speed > 0 and self.x > window_w + self.w:
			self.x = -self.w
		elif self.speed < 0 and self.x < -self.w:
			self.x = window_w

	def draw(self, surface):
		surface.blit(self.image, (self.x, self.y))



