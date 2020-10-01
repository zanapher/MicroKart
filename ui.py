import pyglet
from pyglet.gl import *

from vector import Vector


class UI(object):
    """User interface layout"""

    def __init__(self, window, race):
        self.window = window
        self.race = race
        self.mapshift_x = 200  # how much the map must be shifted because of UI
        self.map_x = self.mapshift_x
        self.map_y = 0
        self.map_zoom = 2
        self.group = pyglet.graphics.OrderedGroup(10)
        self.dark_bg = self.window.batch.add(6, GL_TRIANGLES, self.group, ('v2i', (
        0, 0, 0, self.window.height, self.mapshift_x, self.window.height, 0, 0, self.mapshift_x, self.window.height,
        self.mapshift_x, 0)), ('c4B', (0, 0, 0, 200) * 6))

    def fix_shift_map(self):
        """forbid the map to be shifted more than what the window can display"""
        if self.window.width >= self.mapshift_x + 1024 * self.map_zoom:
            self.map_x = self.mapshift_x
        else:
            if self.map_x > self.mapshift_x:
                self.map_x = self.mapshift_x
            elif self.map_x < -1024 * self.map_zoom + self.window.width:
                self.map_x = -1024 * self.map_zoom + self.window.width
        if self.window.height >= 1024 * self.map_zoom:
            self.map_y = self.window.height - 1024 * self.map_zoom
        else:
            if self.map_y > 0:
                self.map_y = 0
            elif self.map_y < -1024 * self.map_zoom + self.window.height:
                self.map_y = -1024 * self.map_zoom + self.window.height

    def get_map_position(self, x, y):
        """convert window coordinates into map coordinates"""
        return Vector((x - self.map_x) / self.map_zoom, (y - self.map_y) / self.map_zoom)

    def center_map(self, position):
        """center the view on a given position"""
        x, y = position.pair()
        self.map_x = self.window.width / 2 + self.mapshift_x / 2 - x * self.map_zoom
        self.map_y = self.window.height / 2 - y * self.map_zoom
        self.fix_shift_map()

    def shift_map(self, x, y):
        """shift the map"""
        self.map_x += x
        self.map_y += y
        self.fix_shift_map()

    def change_zoom(self, incr=1):
        """change the zoom level"""
        zoom_levels = [.5, 1, 1.5, 2]  # possible zoom levels (cyclic)
        center = self.get_map_position((self.window.width + self.mapshift_x) / 2, self.window.height / 2)
        self.map_zoom = zoom_levels[(zoom_levels.index(self.map_zoom) + incr) % len(zoom_levels)]
        self.center_map(center)

    def update(self):
        """update the UI"""
        h = self.window.height - 60  # vertical position of the first racer icon
        for i, r in enumerate(self.race.racers):
            r.rank = i  # update rank
            r.photo.position = 20, h - 50 * r.rank  # reorder racer icons
            r.item_sprite.position = 52, h - 50 * r.rank
            r.lap_sprite.position = 84, h - 50 * r.rank
            r.lap_times_label.x = 106
            r.lap_times_label.y = h - 50 * r.rank
        self.center_map(self.race.player1.car.position)
