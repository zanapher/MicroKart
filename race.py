import pyglet

from racer import Racer
from track import Track


class Race(object):
    def __init__(self, window, track_num, characters, laps=3):
        self.window = window
        self.track = Track(window, self, track_num)
        self.racers = []
        self.laps = laps
        self.time = 0.  # current time in the race (will be set to 0 when the first racer starts)

        # the time counter
        self.time_label = pyglet.text.Label(color=(230, 230, 230, 255), bold=True, batch=window.batch)
        self.time_label.x = 10
        self.time_label.y = self.window.height - 30

        for i, char in enumerate(characters):
            self.racers.append(Racer(self, i, char))
        self.player1 = self.racers[0]
        if len(self.racers) >= 2:
            self.player2 = self.racers[1]
        else:
            self.player2 = None

        self.particles = []  # list of moving objects other than cars

    def update(self, dt):
        self.racers.sort()  # sort racers according to progression
        self.time += dt
        int_time = int(self.time * 100)
        minutes = int_time / 6000
        seconds = (int_time / 100) % 60
        hundredths = int_time % 100
        self.time_label.text = "Time: %02d' %02d\" %02d" % (minutes, seconds, hundredths)
        for p in self.particles:
            p.update(dt)
        for r in self.racers:
            r.update(dt)
        self.track.update(dt)
        self.window.ui.update()
