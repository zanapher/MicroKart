#!/usr/bin/env python
# encoding: utf-8
"""
microkart.py

Created by Zanapher on 2012-03-01.
"""

import sys
import os
import pyglet
import pyglet.window.key as key
from pyglet.gl import *

pyglet.resource.path = ['resources', 'resources/characters', 'resources/tracks']
pyglet.resource.reindex()

from character import BOWSER, DKJR, KOOPA, LUIGI, MARIO, PEACH, TOAD, YOSHI
from ui import UI
from track import Track
from race import Race

def update(dt):
	window.race.update(dt)
	window.ui.update()

def main():
	global window
	config = Config(sample_buffers=1, samples=2, double_buffer=True, alpha_size=8)
	window = pyglet.window.Window(1024, 768, config=config, resizable=True) # current window
	window.batch = pyglet.graphics.Batch() # all the elements to draw will go in this batch
	window.hidden_batch = pyglet.graphics.Batch() # the elements that are currently not shown
	glEnable(GL_LINE_SMOOTH) # enable anti-aliasing
	glHint (GL_LINE_SMOOTH_HINT, GL_NICEST);
	glEnable(GL_BLEND) # enable transparency
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);	
	@window.event
	def on_draw():
		window.clear()
		window.batch.draw()
		window.fps_display.draw() # draw FPS counter
	
	@window.event
	def on_resize(width, height):
		window.race.time_label.y = height - 30
		window.ui.dark_bg.vertices = (0,0,0,height, window.ui.mapshift_x, height, 0, 0, window.ui.mapshift_x, height, window.ui.mapshift_x,0)
		window.ui.fix_shift_map()
	
	@window.event
	def on_key_press(symbol, modifiers):
		if symbol is key.Z:
		# change zoom
			window.ui.change_zoom()
		
		# *** Player 1 controls *** (flags must be updated on key release too)
		elif symbol is key.UP: # accelerate
			window.race.player1.input_accelerate = True
		elif symbol is key.DOWN: # brake
			window.race.player1.input_brake = True
		elif symbol is key.LEFT: # turn left
			window.race.player1.input_left = True
		elif symbol is key.RIGHT: # turn right
			window.race.player1.input_right = True
		elif symbol is key.ENTER: # use item
			window.race.player1.use_item()
		elif symbol is key.SPACE: # jump
			window.race.player1.jump()
		# *** Player 2 controls *** (flags must be updated on key release too)
		elif symbol is key.W: # accelerate
			window.race.player2.input_accelerate = True
		elif symbol is key.S: # brake
			window.race.player2.input_brake = True
		elif symbol is key.A: # turn left
			window.race.player2.input_left = True
		elif symbol is key.D: # turn right
			window.race.player2.input_right = True
		elif symbol is key.LSHIFT: # use item
			window.race.player2.use_item()
		elif symbol is key.X: # jump
			window.race.player2.jump()
		# free items for player 1
		elif symbol is key._1:
			window.race.player1.get_item(1)
		elif symbol is key._2:
			window.race.player1.get_item(2)
		elif symbol is key._3:
			window.race.player1.get_item(3)
		elif symbol is key._4:
			window.race.player1.get_item(4)
		elif symbol is key._5:
			window.race.player1.get_item(5)
		elif symbol is key._6:
			window.race.player1.get_item(6)
		elif symbol is key._7:
			window.race.player1.get_item(7)
		elif symbol is key._8:
			window.race.player1.get_item(8)
		elif symbol is pyglet.window.key.T:
			window.race.player1.car.spin()
	
	@window.event
	def on_key_release(symbol, modifiers):
		# *** Player 1 controls ***
		if symbol is key.UP:
			window.race.player1.input_accelerate = False
		elif symbol is key.DOWN:
			window.race.player1.input_brake = False
		elif symbol is key.LEFT:
			window.race.player1.input_left = False
		elif symbol is key.RIGHT:
			window.race.player1.input_right = False
		# *** Player 2 controls ***
		if symbol is key.W:
			window.race.player2.input_accelerate = False
		elif symbol is key.S:
			window.race.player2.input_brake = False
		elif symbol is key.A:
			window.race.player2.input_left = False
		elif symbol is key.D:
			window.race.player2.input_right = False

	window.race = Race(window, 15, [PEACH, BOWSER, MARIO, KOOPA, YOSHI, DKJR, TOAD, LUIGI])
	window.ui = UI(window, window.race)
	pyglet.clock.schedule(update)
	window.fps_display = pyglet.clock.ClockDisplay() # FPS counter
	pyglet.app.run()

if __name__ == '__main__':
	main()

