import pyglet

from vector import Vector, bresenham
import math
from track import WALL, DEEP, GRASS, ROAD, JUMP, BOOST, FINISH, START, ITEM, EMPTY
from graphics import sprite_seq

class PowerUp(object):
	def __init__(self, image, name):
		self.image = image
		self.name = name
	def on_use(self, race, racer, alternate):
		pass

class PowerUpNone(PowerUp):
	def __init__(self):
		super(PowerUpNone, self).__init__(sprite_seq['item empty'], "None")

class PowerUpCoin(PowerUp):
	def __init__(self):
		super(PowerUpCoin, self).__init__(sprite_seq['item coins'], "Coins")
	def on_use(self, race, racer, alternate):
		racer.car.state.coins += 5

class PowerUpBanana(PowerUp):
	def __init__(self):
		super(PowerUpBanana, self).__init__(sprite_seq['item banana'], "Banana")
	def on_use(self, race, racer, alternate):
		safe_distance = 8 + racer.car.get_radius() # the radius of a banana is 4
		position = racer.car.position - racer.car.get_direction_vector().normalize(safe_distance)
		if not race.track.type(position) in [WALL, DEEP]:
		# banana cannot appear in deep ground or wall
			return ParticleBanana(race, position)

class PowerUpMushroom(PowerUp):
	def __init__(self):
		super(PowerUpMushroom, self).__init__(sprite_seq['item mushroom'], "Mushroom")
	def on_use(self, race, racer, alternate):
		racer.car.state.change(mushroom=1.)
		if racer.car.speed.norm() < 400.:
			racer.car.set_speed(racer.car.speed.normalize(400.))

class PowerUpGreenShell(PowerUp):
	def __init__(self):
		super(PowerUpGreenShell, self).__init__(sprite_seq['item green shell'], "Green Shell")
	def on_use(self, race, racer, alternate):
		safe_distance = 8 + racer.car.get_radius() # the radius of a green shell is 4
		if alternate: # shell is shot slowly backwards
			position = racer.car.position - racer.car.get_direction_vector().normalize(safe_distance)
			direction = racer.car.get_direction() + math.pi # shell goes backwards
			speed = 80
		else:
			position = racer.car.position + racer.car.get_direction_vector().normalize(safe_distance)
			direction = racer.car.direction
			speed = max(racer.car.speed.norm() + 50, 200)
		if not race.track.type(position) in [WALL, DEEP]:
		# sheel cannot appear on deep ground or wall
			return ParticleGreenShell(race, position, direction, speed)

class PowerUpRedShell(PowerUp):
	def __init__(self):
		super(PowerUpRedShell, self).__init__(sprite_seq['item red shell'], "Red Shell")
	def on_use(self, race, racer, alternate):
		safe_distance = 8 + racer.car.get_radius() # the radius of a red shell is 4
		position = racer.car.position + racer.car.get_direction_vector().normalize(safe_distance)
		direction = racer.car.get_direction()
		speed = max(racer.car.speed.norm() + 50, 200)
		rank = race.racers.index(racer)
		if rank == 0:
			target = None # racer is in first place, no target
		else:
			target = race.racers[rank-1].car # target the car in front
		if not race.track.type(position) in [WALL, DEEP]:
		# sheel cannot appear on deep ground or wall
			return ParticleRedShell(race, position, direction, speed, target)

class PowerUpFeather(PowerUp):
	def __init__(self):
		super(PowerUpFeather, self).__init__(sprite_seq['item feather'], "Feather")
	def on_use(self, race, racer, alternate):
		if not racer.car.state.aerial and not racer.car.state.jump:
			racer.car.state.change(aerial=.5)

class PowerUpLightning(PowerUp):
	def __init__(self):
		super(PowerUpLightning, self).__init__(sprite_seq['item lightning'], "Lightning")
	def on_use(self, race, racer, alternate):
		for opponent in race.racers:
			if opponent != racer and opponent.car.is_vulnerable():
				opponent.car.state.change(lightning=3.)
				opponent.car.stop()

class PowerUpStar(PowerUp):
	def __init__(self):
		super(PowerUpStar, self).__init__(sprite_seq['item star'], "Star")
	def on_use(self, race, racer, alternate):
		pass

# create the pool of possible PowerUps
ITEMS = [PowerUpNone(), PowerUpCoin(), PowerUpBanana(), PowerUpMushroom(), PowerUpGreenShell(), PowerUpRedShell(), PowerUpFeather(), PowerUpLightning(), PowerUpStar()]

class Particle(object):
	def __init__(self, race, position, image, radius=4):
		self.race = race
		self.sprite = pyglet.sprite.Sprite(image, batch=race.window.batch, group=race.track.cars_group)
		self.set_position(position)
		self.radius = radius
		self.vulnerable = True # particles can be destroyed by other elements
		self.removed = False
		race.particles.append(self)
	
	def update(self, dt):
		pass
	
	def get_direction_vector(self):
		"""returns the direction as a unit vector (only possible for moving particles)"""
		return Vector(math.cos(self.direction), math.sin(self.direction))
	
	def get_position(self):
		return self.position
	
	def set_position(self, new_position):
		"""this function is called whenever the position of the particle changes"""
		self.position = new_position
		self.sprite.position = self.position.pair()
	
	def set_speed(self, new_speed):
		self.speed = new_speed

	def check_collisions(self):
		"""check for collisions with other particles or cars"""
		for p in self.race.particles:
			if self.removed:
				return
			if p != self and p.vulnerable and self.position.distance(p.position) <= self.radius + p.radius:
				self.particle_collision(p)
		for r in self.race.racers:
			if self.removed:
				return
			if self.position.distance(r.car.position) <= self.radius + r.car.get_radius() and not r.car.state.aerial:
				self.car_collision(r.car)
	
	def particle_collision(self, particle):
		pass
	
	def car_collision(self, car):
		pass
	
	def remove(self):
		self.removed = True
		self.race.particles.remove(self)
		self.sprite.delete()

class ParticleBanana(Particle):
	"""a banana peel that remains on the track until something hits it"""
	color = (248, 248, 0)
	name = "Banana"
	def __init__(self, race, position):
		super(ParticleBanana, self).__init__(race, position, sprite_seq['banana'], 4)
	
	def update(self, dt):
		self.check_collisions()
	
	def car_collision(self, car):
		self.remove()
		if car.is_vulnerable():
			car.stop()

class ParticleGreenShell(Particle):
	"""a green shell that bounces across the track"""
	color = (64, 224, 64)
	name = "Green Shell"
	def __init__(self, race, position, direction, speed):
		super(ParticleGreenShell, self).__init__(race, position, sprite_seq['green shell'], 4)
		self.direction = direction
		self.speed = speed
	def update(self, dt):
		track = self.race.track
		current_position = self.position
		move = self.get_direction_vector() * self.speed * dt
		new_position = current_position + move
		path = bresenham(current_position, new_position)
		for i, c in enumerate(path):
			if track.type(c, hit=True) == WALL:
			# the shell bounces
				if c[0] != path[i-1][0]: # vertical wall
					self.direction = -self.direction + math.pi
				else: # horizontal wall
					self.direction = -self.direction
				new_position = current_position # don't move
				self.set_speed(self.speed - 15.) # slow down after each bounce
				if self.speed <= 40:
					return self.remove() # if the shell becomes too slow it disappears
				break
			elif track.type(new_position) == DEEP:
			# the shell disappears
				return self.remove()
		self.set_position(new_position)
		self.check_collisions()
	
	def car_collision(self, car):
		self.remove()
		if car.is_vulnerable():
			car.stop()
	
	def particle_collision(self, p):
			p.remove()
			self.remove()

class ParticleRedShell(Particle):
	"""a homing red shell aimed at a car (or possibly nothing if it had no target when shot)"""
	color = (248, 0, 0)
	name = "Red Shell"
	def __init__(self, race, position, direction, speed, target):
		super(ParticleRedShell, self).__init__(race, position, sprite_seq['red shell'], 4)
		self.direction = direction
		self.turn = 2.
		self.speed = speed
		self.target = target
	
	def update(self, dt):
		track = self.race.track
		current_position = self.position
		if not self.target is None:
			target_direction = (self.target.position - self.position).angle()
			direction_variation = ((target_direction - self.direction + math.pi) % (2*math.pi)) - math.pi
			if direction_variation > self.turn * dt:
				direction_variation = self.turn * dt
			elif direction_variation < -self.turn * dt:
				direction_variation = -self.turn * dt
			self.direction += direction_variation
		move = self.get_direction_vector() * self.speed * dt
		new_position = current_position + move
		path = bresenham(current_position, new_position)
		for i, c in enumerate(path):
			if track.type(c, hit=True) in [WALL, DEEP]:
			# the shell hits a wall or a hole and disappears
				return self.remove()
		self.set_position(new_position)
		self.check_collisions()
	
	def car_collision(self, car):
		self.remove()
		if car.is_vulnerable():
			car.stop()
	
	def particle_collision(self, p):
			p.remove()
			self.remove()
