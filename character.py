import pyglet

class Character(object):
	def __init__(self, sprite_sheet, name, color, color_dark, acceleration, turn_speed, max_speed, grass_penalty, radius):
		img = pyglet.resource.image(sprite_sheet)
		seq = pyglet.image.ImageGrid(img, 2, 11)  # the sprite images for the car
		for image in seq:
			image.anchor_x = 16
			image.anchor_y = 8
		self.name = name
		self.color = color
		self.acceleration = acceleration
		self.turn_speed = turn_speed
		self.max_speed = max_speed
		self.radius = radius
		self.grass_penalty = grass_penalty
		self.sprite_seq = seq
		self.photo = seq[0]

BOWSER = Character('ch_bowser.png', 'Bowser', (250, 187, 0), (186, 120, 0), 20, 1, 150, .75, 8)
DKJR = Character('ch_dkjr.png', 'Donkey Kong Jr.', (180, 0, 0), (122,0,0), 20, 1, 150, .75, 8)
KOOPA = Character('ch_koopa.png', 'Koopa', (0, 248, 0), (0, 179, 0), 30, 1, 70, .4, 4)
LUIGI = Character('ch_luigi.png', 'Luigi', (0, 248, 0), (0, 179, 0), 25, 1, 100, .5, 6)
MARIO = Character('ch_mario.png', 'Mario', (255, 0, 0), (160, 0, 0), 25, 1, 100, .5, 6)
TOAD = Character('ch_toad.png', 'Toad', (228, 172, 138), (169, 120, 89), 30, 1, 70, .4, 4)
YOSHI = None

DKJR = {
	'sprite_seq': 'ch_dkjr.png',
	'name': 'Donkey Kong Jr.',
	'color': (180, 0, 0),
	'acceleration': 300.,
	'brake': 2.,
	'turn': 3.,
	'mass': 2.,
	'friction': 1.,
	'adhesion': 1200.,
	'radius': 8,
}
PEACH = {
	'sprite_seq': 'ch_peach.png',
	'name': 'Peach',
	'color': (242, 184, 169),
	'acceleration': 200.,
	'brake': 2.,
	'turn': 3.,
	'mass': 1.,
	'friction': 1.,
	'adhesion': 300.,
	'radius': 8,
}

for c in [DKJR, PEACH]:
	img = pyglet.resource.image(c['sprite_seq'])
	c['sprite_seq'] = pyglet.image.ImageGrid(img, 2, 11)  # the sprite images for the car
	for image in c['sprite_seq']:
		image.anchor_x = 16
		image.anchor_y = 8