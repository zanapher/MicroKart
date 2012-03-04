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
		img = pyglet.resource.image(sprite_sheet)
		self.sprite_seq = pyglet.image.ImageGrid(img, 2, 11)  # the sprite images for the car
		for image in self.sprite_seq:
			image.anchor_x = 16
			image.anchor_y = 8
		self.photo = self.sprite_seq[0]

BOWSER = Character(
	sprite_sheet = 'ch_bowser.png',
	name = 'Bowser',
	color = (250, 187, 0),
	acceleration = 300.,
	turn_speed = 3.,
	mass = 2.,
	friction = 1.,
	adhesion = 600.,
	radius = 8)

DKJR = Character(
	sprite_sheet = 'ch_dkjr.png',
	name = 'Donkey Kong Jr.',
	color = (180, 0, 0),
	acceleration = 300.,
	turn_speed = 3.,
	mass = 2.,
	friction = 1.,
	adhesion = 600.,
	radius = 8)

KOOPA = Character(
	sprite_sheet = 'ch_koopa.png',
	name = 'Koopa',
	color = (0, 248, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

LUIGI = Character(
	sprite_sheet = 'ch_luigi.png',
	name = 'Luigi',
	color = (0, 248, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

MARIO = Character(
	sprite_sheet = 'ch_mario.png',
	name = 'Mario',
	color = (255, 0, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

PEACH = Character(
	sprite_sheet = 'ch_peach.png',
	name = 'Peach',
	color = (242, 184, 169),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

TOAD = Character(
	sprite_sheet = 'ch_toad.png',
	name = 'Toad',
	color = (228, 172, 138),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)

YOSHI = Character(
	sprite_sheet = 'ch_yoshi.png',
	name = 'Yoshi',
	color = (0, 248, 0),
	acceleration = 200.,
	turn_speed = 3.,
	mass = 1.,
	friction = 1.,
	adhesion = 300.,
	radius = 8)
