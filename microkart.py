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
	glDisable(GL_LINE_SMOOTH) # enable anti-aliasing
#	glHint (GL_LINE_SMOOTH_HINT, GL_NICEST);
	glEnable(GL_BLEND) # enable transparency
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	@window.event
	def on_draw():
		window.clear()
		window.batch.draw()
	
	@window.event
	def on_resize(width, height):
		window.race.time_label.y = height - 30
		window.ui.dark_bg.vertices = (0,0,0,height, window.ui.mapshift_x, height, 0, 0, window.ui.mapshift_x, height, window.ui.mapshift_x,0)
		window.ui.fix_shift_map()
	
	@window.event
	def on_key_press(symbol, modifiers):
		if symbol == key.Z:
		# change zoom
			window.ui.change_zoom()
		
		# *** Player 1 controls *** (flags must be updated on key release too)
		elif symbol == key.UP: # accelerate
			window.race.player1.input_accelerate = True
		elif symbol == key.DOWN: # brake
			window.race.player1.input_brake = True
		elif symbol == key.LEFT: # turn left
			window.race.player1.input_left = True
		elif symbol == key.RIGHT: # turn right
			window.race.player1.input_right = True
		elif symbol == key.ENTER: # use item
			window.race.player1.use_item()
		elif symbol == key.SPACE: # jump
			window.race.player1.jump()
		# *** Player 2 controls *** (flags must be updated on key release too)
		elif symbol == key.W: # accelerate
			window.race.player2.input_accelerate = True
		elif symbol == key.S: # brake
			window.race.player2.input_brake = True
		elif symbol == key.A: # turn left
			window.race.player2.input_left = True
		elif symbol == key.D: # turn right
			window.race.player2.input_right = True
		elif symbol == key.LSHIFT: # use item
			window.race.player2.use_item()
		elif symbol == key.X: # jump
			window.race.player2.jump()
		# free items for player 1
		elif symbol == key._1:
			window.race.player1.get_item(1)
		elif symbol == key._2:
			window.race.player1.get_item(2)
		elif symbol == key._3:
			window.race.player1.get_item(3)
		elif symbol == key._4:
			window.race.player1.get_item(4)
		elif symbol == key._5:
			window.race.player1.get_item(5)
		elif symbol == key._6:
			window.race.player1.get_item(6)
		elif symbol == key._7:
			window.race.player1.get_item(7)
		elif symbol == key._8:
			window.race.player1.get_item(8)
		elif symbol == pyglet.window.key.T:
			print window.race.particles
	
	@window.event
	def on_key_release(symbol, modifiers):
		# *** Player 1 controls ***
		if symbol == key.UP:
			window.race.player1.input_accelerate = False
		elif symbol == key.DOWN:
			window.race.player1.input_brake = False
		elif symbol == key.LEFT:
			window.race.player1.input_left = False
		elif symbol == key.RIGHT:
			window.race.player1.input_right = False
		# *** Player 2 controls ***
		if symbol == key.W:
			window.race.player2.input_accelerate = False
		elif symbol == key.S:
			window.race.player2.input_brake = False
		elif symbol == key.A:
			window.race.player2.input_left = False
		elif symbol == key.D:
			window.race.player2.input_right = False

	window.race = Race(window, 11, [PEACH, BOWSER, KOOPA, TOAD, MARIO, LUIGI, YOSHI, DKJR])
	window.ui = UI(window, window.race)
	pyglet.clock.schedule(update)
	pyglet.app.run()

if __name__ == '__main__':
	main()

