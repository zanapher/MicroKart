import pyglet
from pyglet.gl import *

from graphics import sprite_seq
from vector import Vector, bresenham

# self.data
WALL = chr(0)
GHOST = chr(40)
DEEP = chr(50)
GRASS = chr(127)
ROAD = chr(255)
JUMP = chr(180)
BOOST = chr(220)
# self.special_data
FINISH = chr(0)
START = chr(50)
ITEM = chr(200)
EMPTY = chr(255)


class Track_Group(pyglet.graphics.OrderedGroup):
    def __init__(self, order, window):
        super(Track_Group, self).__init__(order)
        self.window = window

    def set_state(self):
        glPushMatrix()
        glTranslatef(self.window.ui.map_x, self.window.ui.map_y, 0)
        glScalef(self.window.ui.map_zoom, self.window.ui.map_zoom, 0.)

    def unset_state(self):
        glPopMatrix()


class Track(object):
    """representation of the track"""

    def __init__(self, window, race, track_num):
        super(Track, self).__init__()
        self.window = window
        self.race = race

        # create the drawing groups
        self.bg_group = Track_Group(0, window)  # the background map image
        self.objects_group = Track_Group(1, window)  # the track elements (item blocks, breakable walls, etc.)
        self.shadows_group = Track_Group(2, window)  # cars shadows
        self.cars_group = Track_Group(3, window)  # the cars and particles

        # load the image files to create the track
        self.track_num = track_num
        self.map = pyglet.sprite.Sprite(pyglet.resource.image("%s.png" % track_num), batch=window.batch,
                                        group=self.bg_group)
        self.data = pyglet.resource.file("%st.pgm" % track_num).read()[15:]
        self.special_data = pyglet.resource.file("%ss.pgm" % track_num).read()[15:]
        self.beacons = self.make_beacons()
        self.objects = {}

        # create the track's special elements
        self.item_blocks = {}  # dictionary of item blocks indexed by the small coordinates (128x128) of their NE corner
        self.item_blocks_list = []  # list of item blocks to update at the end of each turn
        self.start_positions = []
        # Parse data to place special objects (coins, vanishing wall, ice blocks)
        for i, c in enumerate(self.data):
            if c is GHOST:
                x, y = i % 128, 127 - i / 128
                self.objects[(x, y)] = ObjectGhostWall(self, x, y)
        # Parse special data for track elements (finish line, starting positions, etc.)
        for i, c in enumerate(self.special_data):
            if c is FINISH and not self.special_data[i - 1] is FINISH:
                # left extremity of the finish line
                finish_x1 = (i % 128) * 8
                finish_y = (127 - i / 128) * 8
            elif c is FINISH and not self.special_data[i + 1] is FINISH:
                # right extremity of the finish line
                finish_x2 = (i % 128) * 8 + 8
                self.finish_line = (finish_x1, finish_x2, finish_y)  # coordinates of the finish line
            if c is START:
                # starting position
                self.start_positions.append(Vector((i % 128) * 8 + 8, (127 - i / 128) * 8 + 4))
            elif c is ITEM:
                # item block
                x, y = i % 128, 127 - i / 128
                if not (x, y) in self.item_blocks.keys():
                    new_block = ObjectItemBlock(self, (x + 1), y)
                    self.item_blocks_list.append(new_block)
                    self.item_blocks[(x, y)] = new_block  # an item block spans 4 cells in the 128x128 map
                    self.item_blocks[(x + 1, y)] = new_block
                    self.item_blocks[(x + 1, y - 1)] = new_block
                    self.item_blocks[(x, y - 1)] = new_block
        # Beacons map
        try:
            self.beacons_map = pyglet.resource.file("%sbm.pgm" % track_num).read()[15:]
        except pyglet.resource.ResourceNotFoundException:
            print
            "Beacons map not found, creating one."
            self.make_beacons_map()
            pyglet.resource.reindex()
            self.beacons_map = pyglet.resource.file("%sbm.pgm" % track_num).read()[15:]

    def make_beacons(self):
        """computes the sequence of beacon points from the beacons file"""
        bstring = pyglet.resource.file('%sb.pgm' % self.track_num).read()[15:]
        beacons = []
        remaining = []
        for i, c in enumerate(bstring):
            if c is chr(0):  # a new beacon was found
                remaining.append(Vector(i % 128, 127 - i / 128))
            elif c is chr(127):  # first or second beacon
                beacons.insert(0, Vector(i % 128, 127 - i / 128))
        while remaining != []:
            b1 = beacons[-1]
            new_beacon = min(remaining, key=lambda b: (b.x - b1.x) ** 2 + (b.y - b1.y) ** 2)
            beacons.append(new_beacon)
            remaining.remove(new_beacon)
        print
        "%s beacons created." % len(beacons)
        return beacons

    def make_beacons_map(self):
        """computes for each point of the map (128x128) the closest beacon in sight"""

        def in_sight(p1, p2):
            """returns True if the straight path from p1 to p2 has no obstacle"""
            path = bresenham(p1, p2)
            for c in path:
                x, y = c.pair()
                if self.data[x + 128 * (127 - y)] is WALL or self.special_data[x + 128 * (127 - y)] is FINISH:
                    return False
            return True

        def find_beacon(position):
            """returns the id of the closest beacon that is in line of sight"""
            beacons = self.beacons
            x, y = position.pair()
            if self.data[x + 128 * (127 - y)] is WALL:
                return 255
            if self.special_data[x + 128 * (127 - y)] is FINISH:
                return 0
            min_distance = float("infinity")
            bid = None
            for i, v in enumerate(beacons):
                if position.distance(v) < min_distance and in_sight(position, v):
                    min_distance = position.distance(v)
                    bid = i
            if not bid is None:
                return bid
            for i, v in enumerate(beacons):
                if position.distance(v) < min_distance:
                    min_distance = position.distance(v)
                    bid = i
            return bid

        output = open('resources/tracks/%sbm.pgm' % self.track_num, 'w')
        output.write("P5\n128 128\n255\n")

        for j in range(127, -1, -1):  # vertical coordinate
            print
            "line %s." % j
            for i in range(128):  # horizontal coordinate
                output.write(chr(find_beacon(Vector(i, j))))
        output.close()

    def get_beacon_id(self, position):
        """returns the index of the current beacon"""
        return ord(self.beacons_map[int(position.x) / 8 + 128 * (127 - int(position.y) / 8)])

    def get_beacon(self, position):
        """returns the beacon that corresponds to the given position"""
        bid = self.get_beacon_id(position)
        return Vector(self.beacons[bid].x * 8, self.beacons[bid].y * 8)

    def type(self, position, special=False, hit=False):
        """returns the track type at given position (position can be a vector in big coordinates or a pair of small coordinates)"""
        if isinstance(position, Vector):
            x, y = int(position.x) / 8, int(position.y) / 8
        else:
            x, y = position
        i = x + 128 * (127 - y)
        if special:
            if not (0 <= x < 128 and 0 <= y < 128):  # out of map
                return EMPTY
            return self.special_data[i]
        else:
            if not (0 <= x < 128 and 0 <= y < 128):  # out of map
                return WALL
            data = self.data[i]
            if data is GHOST:  # ghost house vanishing wall
                if (x, y) in self.objects:
                    if hit:
                        self.objects.pop((x, y))
                    return WALL
                else:
                    return DEEP
            else:
                return data

    def ground_friction(self, position):
        """returns the ground friction coefficient corresponding to the given position on the track"""
        ground_type = self.type(position)
        if ground_type is GRASS:
            return 50.
        else:
            return 10.

    def update(self, dt):
        """update the track elements"""
        for block in self.item_blocks_list:
            block.update(dt)


class ObjectItemBlock(object):
    """A '?' block that gives a powerup when a car passes on it"""

    def __init__(self, track, x, y):
        self.track = track
        self.delay = 0.  # time before it is active again (after being used)
        self.sprite = pyglet.sprite.Sprite(sprite_seq['item block'], 8 * x, 8 * y, batch=self.track.window.batch,
                                           group=track.objects_group)

    def update(self, dt):
        if self.delay > 0:
            self.delay -= dt
            if self.delay <= 0:
                self.delay = 0
                self.sprite.image = sprite_seq['item block']

    def activate(self):
        self.delay = 15.
        self.sprite.image = sprite_seq['item block empty']


class ObjectGhostWall(object):
    """A wall that disappears when hit by a car or particle"""

    def __init__(self, track, x, y):
        self.track = track
        self.sprite = pyglet.sprite.Sprite(sprite_seq['ghost wall'], 8 * x + 4, 8 * y + 4, batch=track.window.batch,
                                           group=track.objects_group)
