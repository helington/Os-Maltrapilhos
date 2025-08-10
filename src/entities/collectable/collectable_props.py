from ..entities_enum import Collectable_item

class Collectable_Props:
    def __init__(self, x, y, item: Collectable_item):
        self.x = x
        self.y = y
        self.__dict__.update(item.value)


