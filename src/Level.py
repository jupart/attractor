class Point():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Level():
    names = []
    points = []
    rotations = []

    def __init__(self, **kwargs):
        pass

    def add_entity(self, name, x, y, rot):
        self.names.append(name)
        self.points.append(Point(x, y))
        self.rotations.append(rot)

    def empty(self):
        if self.names == []:
            return True
        else:
            return False

    def pop_entity(self):
        return self.names.pop(), self.points.pop(), self.rotations.pop()

    def clear(self):
        self.names.clear()
        self.points.clear()
        self.rotations.clear()