import pygame

"""
Contains the timers classes.
"""

# TIMERS
class CooldownTimer():
	"""
	A timer, based on a cooldown. Not recommended.
	"""
	def __init__(self,cooldown:int):

		self.cooldown = cooldown
		self.timer = cooldown
		self.finished = False

	def update(self,dt:float=1.0)->None:
		"""
		Update the timer.
		"""
		# decrease timer value
		self.timer -= 1*dt
		if self.timer <= 0:
		# set the status finished to true
			self.finished = True
			self.timer = 0

	def reset(self)->None:
		"""
		Reset the timer.
		"""
		# reset the variables
		self.timer = self.cooldown
		self.finished = False

class Timer:
	"""
	A timer based on game ticks.
	"""
	def __init__(self,duration:int,func = None,start_active=False):
		self.duration = duration 
		self.func = func
		self.start_time = 0
		self.active = False
		if start_active:
			self.activate()

	def activate(self)->None:
		"""
		Activate the timer.
		"""
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self)->None:
		"""
		Deactivate the timer.
		"""
		self.active = False
		self.start_time = 0

	def update(self,activate_on_end=False)->None:
		"""
		Update the timer.
		"""
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time> self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()
			if activate_on_end:
				self.activate()

