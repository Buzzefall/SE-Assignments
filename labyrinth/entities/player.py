from common.enum import Direction
from entities.base import Entity
from entities.cell import Cell
from events.base import Listener, Event
from events.events import EnteredCellEvent, TreasureFoundEvent
from events.system import EventSystem


class PlayerInventory(Entity):
    def __init__(self):
        super().__init__()
        self.container = {}

    def search(self, item_name: str) -> list:
        return [item for item in self.container if item.name == item_name]

    def has(self, item: Entity):
        if item in self.container:
            return True
        else:
            return False

    def add(self, item: Entity):
        self.container[item.name] = item

    def remove(self, item: Entity):
        if item.name in self.container:
            del self.container[item.name]


class Player(Entity):
    def __init__(self, name: str, location: Cell):
        super().__init__()
        self.name = name
        self.cell = location
        self.inventory = PlayerInventory()

    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.cell = self.cell.left
        elif direction == Direction.RIGHT:
            self.cell = self.cell.right
        elif direction == Direction.UP:
            self.cell = self.cell.up
        elif direction == Direction.DOWN:
            self.cell = self.cell.down

        treasure = self.cell.find_treasure()
        if treasure is not None:
            self.inventory.add(treasure)
            EventSystem().register(TreasureFoundEvent(treasure, target=self.cell))
