import pyglet

class Character(object):
	def __init__(self, sprite_sheet, name, color, acceleration, turn_speed, mass, friction, adhesion, radius):
		self.name = name
		self.color = color
		self.acceleration = acceleration
		self.turn_speed = turn_speed
		self.mass = mass
		self.friction = friction
		self.adhesion = adhesion
		self.radius = radius
		# prepare the sprites
		self.sprite_seq = []
		for i in range(22):
			self.sprite_seq.append(pyglet.resource.image(sprite_sheet+"-%d.png" % i))
		for image in self.sprite_seq:
			image.anchor_x = 17
			image.anchor_y = 9
		self.photo = self.sprite_seq[16]

BOWSER = Character(
	sprite_sheet = 'bowser',
	name = 'Bowser',
	color = (250, 187, 0),
	acceleration = 300.,
	turn_speed = 3.,
	mass = 2.,
	friction = 1.,
	adhesion = 600.,
	radius = 8)

DKJR = Character(
	sprite_sheet = 'dkjr',
	name = 'Donkey Kong Jr.',
	color = (180, 0, 0),
	acceleration = 300.,
	turn_speed = 3.,
	mass = 2.,
	friction = 1.,
	adhesion = 600.,
	radius = 8)

KOOPA = Character(
	sprite_sheet = 'koopa',
	name = 'Koopa',
	color = (0, 248, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

LUIGI = Character(
	sprite_sheet = 'luigi',
	name = 'Luigi',
	color = (0, 248, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

MARIO = Character(
	sprite_sheet = 'mario',
	name = 'Mario',
	color = (255, 0, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

PEACH = Character(
	sprite_sheet = 'peach',
	name = 'Peach',
	color = (242, 184, 169),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

TOAD = Character(
	sprite_sheet = 'toad',
	name = 'Toad',
	color = (228, 172, 138),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

YOSHI = Character(
	sprite_sheet = 'yoshi',
	name = 'Yoshi',
	color = (0, 248, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)
