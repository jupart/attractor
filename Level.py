class Point():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Stats():
    ideal_time = 0
    ideal_changes = 0

    def __init__(self, **kwargs):
        self.timer = 0
        self.changes = 0
class Level():
    names = []
    points = []
    rotations = []
    ids = []
    background = None
    background2 = None
    stats = Stats()

    def __init__(self, **kwargs):
        pass

    def add_entity(self, name, x, y, rot, ids):
        self.names.append(name)
        self.points.append(Point(x, y))
        self.rotations.append(rot)
        self.ids.append(ids)

    def empty(self):
        if self.names == []:
            return True
        else:
            return False

    def pop_entity(self):
        return self.names.pop(), self.points.pop(), self.rotations.pop(), self.ids.pop()

    def clear(self):
        del self.names[:]
        del self.points[:]
        del self.rotations[:]
        del self.ids[:]

        self.stats.time = 0
        self.stats.changes = 0


