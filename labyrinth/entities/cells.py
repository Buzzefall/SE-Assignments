from entities.enum import CellType
from entities.base import Entity

from events.base import Listener, Event
from events.events import EnteredCellEvent, LeftCellEvent


class Cell(Entity, Listener):
    def __init__(self, cell_type: CellType, x: int, y: int):
        super().__init__()
        self.type = cell_type
        self.x = x
        self.y = y
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.entities = []

    def add_neighbours(self, neighbours: dict):
        self.up = neighbours['up'] if 'up' in neighbours else None
        self.down = neighbours['down'] if 'down' in neighbours else None
        self.left = neighbours['left'] if 'left' in neighbours else None
        self.right = neighbours['right'] if 'right' in neighbours else None

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

    def find_player(self):
        def is_player(obj):
            return type(obj).__name__ == 'Player'

        for e in self.entities:
            if is_player(e):
                return e

        return None

    def receive(self, event: Event):
        if isinstance(event, EnteredCellEvent):
            self.add_entity(event.source)
        elif isinstance(event, LeftCellEvent):
            self.remove_entity(event.source)

    def __str__(self):
        if self.type == CellType.Monolith:
            return "▧ "
        elif self.type == CellType.Wall:
            return "# "
        elif self.find_player():
            return "℗ "
        elif self.type == CellType.Empty:
            return "  "

# class EmptyCell(Cell):
#     def __init__(self, x: int, y: int):
#         super().__init__(x, y)
#
#
# class WallCell(Cell):
#     def __init__(self, x: int, y: int):
#         super().__init__(x, y)
#
#
# class MonolithCell(Cell):
#     def __init__(self, x: int, y: int):
#         super().__init__(x, y)
