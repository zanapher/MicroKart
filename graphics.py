import pyglet

# prepare the sprites
sprite_seq = pyglet.image.ImageGrid(pyglet.resource.image('sprite_sheet.gif'), 5, 8)
for img in sprite_seq:
	img.anchor_x = img.width / 2
	img.anchor_y = img.height / 2
sprite_seq[37].anchor_x = 30 # the fishing Lakitu
sprite_seq[37].anchor_y = -24
sprite_seq[38].anchor_y = 8 # the shadow sprite
