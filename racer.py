import pyglet
import pyglet.window.key as key
import random

from car import Car
from items import ITEMS
from graphics import sprite_seq

class Racer(object):
	def __init__(self, race, rank, character):
		self.race = race
		self.rank = rank
		self.character = character
		self.car = Car(race, self, character, race.track.start_positions[rank])
		self.photo = pyglet.sprite.Sprite(self.character['sprite_seq'][0], batch=race.window.batch)
		self.state = RacerState()
		self.item = ITEMS[0]
		self.item_sprite = pyglet.sprite.Sprite(self.item.image, batch=race.window.batch)
		self.lap_sprite = pyglet.sprite.Sprite(sprite_seq[-1], batch=race.window.batch)
		self.lap = 0
		self.lap_times = []
		self.lap_times_label = pyglet.text.Label(color=self.character['color']+(255,), font_name="Courier", font_size=10, bold=True, width=200, multiline=True, batch=race.window.batch)
		self.display_times()
		
		# possible duration inputs
		self.input_accelerate = False
		self.input_brake = False
		self.input_left = False
		self.input_right = False
	
	def __cmp__(self, other):
		"""compares the relative advancement of two racers"""
		return self.car.__cmp__(other.car)
	
	def update(self, dt):
		"""update the state of the racer after dt seconds"""		
		# update state
		if self.state.item_rolling > 0:
			self.state.item_rolling = max(0, self.state.item_rolling - dt)
			if self.state.item_rolling == 0:
				self.item_sprite.image = self.item.image
		self.car.update(dt)
	
	def get_item(self, item_id=None):
		if self.item == ITEMS[0]:
			if item_id != None:
				self.item = ITEMS[item_id]
			else:
				self.item = random.choice(ITEMS[1:])
			self.state.item_rolling = 1.
			self.item_sprite.image = sprite_seq[9]
	
	def use_item(self, alternate=False):
		if self.state.active and self.item != ITEMS[0] and self.state.item_rolling == 0:
			self.item.on_use(self.race, self, alternate)
			self.item = ITEMS[0]
			self.item_sprite.image = self.item.image
	
	def jump(self):
		if self.state.active:
			self.car.jump()
	
	def display_times(self):
		def float_to_time(t):
			int_time = int(t * 100)
			minutes = int_time / 6000
			seconds = (int_time / 100) % 60
			hundredths = int_time % 100
			return "%02d' %02d\" %02d" % (minutes, seconds, hundredths)
		empty_time = "--' --\" --\n"
		s = ''
		for i in range(self.race.laps):
			if i < len(self.lap_times):
				s += float_to_time(self.lap_times[i]) + '\n'
			else:
				s += empty_time
		self.lap_times_label.text = s
	
	def new_lap(self, incr=1):
		"""change the number of laps of the racer (going through the finish line)"""
		self.lap += incr # incr can be -1 if going backwards through the line
		if self.lap > len(self.lap_times)+1:
			self.lap_times.append(self.race.time)
			self.display_times()
		if self.lap == self.race.laps:
			self.lap_sprite.image = sprite_seq[35]
		elif self.lap > self.race.laps:
			self.lap_sprite.image = sprite_seq[36]
		elif self.lap == 2:
			self.lap_sprite.image = sprite_seq[32]
		elif self.lap == 3:
			self.lap_sprite.image = sprite_seq[33]
		elif self.lap == 4:
			self.lap_sprite.image = sprite_seq[34]
		else:
			self.lap_sprite.image = sprite_seq[-1]

class RacerState(object):
	"""The current state of a racer"""
	def __init__(self):
		self.item_rolling = 0.
		self.active = True # the player can control the car

