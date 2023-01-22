from __future__ import annotations

from vector2 import Vector2

from collections import defaultdict
from dataclasses import dataclass
from functools import partialmethod
from itertools import chain, product
from heapq import heappush, heappop
from enum import Enum, IntEnum
from time import sleep

from collections.abc import Iterable

LOT_CAR_NAMES = [
    f"\x1b[{i}m%s\x1b[0m"
    for i in chain(range(101, 108), range(41, 48))  # start with 101 to make the main car red
]
LOT_CELL_WIDTH = 2
LOT_MOVING_SYMBOL = "#" * LOT_CELL_WIDTH
LOT_STATIC_SYMBOL = " " * LOT_CELL_WIDTH
LOT_EMPTY_SYMBOL  = " " * LOT_CELL_WIDTH

DEFAULT_PRINT_DELAY_IN_PLACE = 0.5
DEFAULT_PRINT_DELAY          = 0


class Orientation(Vector2, Enum):
    UP    =  0, -1
    DOWN  =  0,  1
    LEFT  = -1,  0
    RIGHT =  1,  0

    HORIZONTAL = 1, 0
    VERTICAL   = 0, 1


class Direction(IntEnum):
    POSITIVE =  1
    NEGATIVE = -1


@dataclass(frozen=True)
class Car:
    orientation: Orientation
    position: Vector2
    size: Vector2

    def moved(self, direction: Direction) -> Car:
        return Car(
            self.orientation,
            self.position + self.orientation * direction,
            self.size
        )


@dataclass(frozen=True)
class Lot:
    cars: tuple[Car, ...]  # first car is main car
    size: Vector2
    exit_direction: Direction

    def print_solution(self, history: Iterable[tuple[int, Direction]], in_place=True, delay=None) -> None:
        """
        recreate then print the steps taken in the solution
        """
        lot = self

        grid_height = self.size.y

        move_count = len(history)
        move_count_length = len(str(move_count))

        print_prefix = ""
        if in_place:
            # add newlines so that the print in the loop doesn't overwrite previous lines in the terminal
            print('\n'*(grid_height + 1))
            print_prefix = f"\x1b[{grid_height + 2}A\x1b[2K"
            if delay is None:
                delay = DEFAULT_PRINT_DELAY_IN_PLACE
        else:
            if delay is None:
                delay = DEFAULT_PRINT_DELAY

        cars = lot.cars
        for i, (car_index, direction) in enumerate(history):
            car = cars[car_index]

            match car.orientation * direction:
                case Orientation.UP:
                    way = "up"
                case Orientation.DOWN:
                    way = "down"
                case Orientation.LEFT:
                    way = "left"
                case Orientation.RIGHT:
                    way = "right"

            print(f"{print_prefix}({str(i+1).rjust(move_count_length)}/{move_count}): move {LOT_CAR_NAMES[car_index] % LOT_MOVING_SYMBOL} {way}")

            cars = (*cars[:car_index], car.moved(direction), *cars[car_index+1:])
            lot = Lot(
                cars,
                lot.size,
                lot.exit_direction
            )

            print(lot.format_move(car_index), end="\n\n")
            sleep(delay)
        
        print(f"solvable in {move_count} moves")
    
    def solve(self) -> None:
        """
        solve the lot with A* then print the solution
        """
        possibilities: list[tuple[int, int, tuple[tuple[int, Direction], ...], Lot]] = [(self.heuristic, 0, (), self)]
        tried: set[Lot] = {self}

        while possibilities:
            _, step_number, history, lot = heappop(possibilities)

            if lot.is_solved:
                return history

            for direction in Direction:
                cars = lot.cars
                for i, car in enumerate(cars):
                    new_cars = (*cars[:i], car.moved(direction), *cars[i+1:])

                    new_lot = Lot(new_cars, lot.size, lot.exit_direction)
                    if new_lot.is_valid and new_lot not in tried:
                        tried.add(new_lot)
                        heappush(possibilities, (
                            new_lot.heuristic,
                            step_number + 1,
                            (*history, (i, direction)), 
                            new_lot
                        ))

        raise ValueError("lot is unsolvable")

    @property
    def heuristic(self) -> int:
        """
        return the distance of the main car from the exit
        """
        main_car = self.main_car
        axis = main_car.orientation is Orientation.VERTICAL
        
        if self.exit_direction is Direction.NEGATIVE:
            return main_car.position[axis]
        else:
            return self.size[axis] - (main_car.position[axis] + main_car.size[axis])

    @property
    def main_car(self) -> Car:
        return self.cars[0]

    @property
    def is_solved(self) -> bool:
        main_car = self.main_car
        axis = main_car.orientation is Orientation.VERTICAL
        
        if self.exit_direction is Direction.NEGATIVE:
            return main_car.position[axis] == 0
        else:
            return main_car.position[axis] + main_car.size[axis] == self.size[axis]

    @property
    def is_valid(self) -> bool:
        occupied_cells: set[tuple[int, int]] = set()
        for car in self.cars:
            x, y = car.position
            w, h = car.size

            if x < 0 or y < 0:
                return False

            if x + w > self.size.x or y + h > self.size.y:
                return False

            car_cells = set(product(range(x, x + w), range(y, y + h)))
            if occupied_cells & car_cells:
                return False
            
            occupied_cells.update(car_cells)
        
        return True

    def format_move(self, last_moved_index: int) -> None:
        """
        print the lot while highlighting the car that moved last
        pass -1 to not highlight any car
        """

        grid: dict[tuple[int, int], str] = defaultdict(lambda: LOT_EMPTY_SYMBOL)

        for i, car in enumerate(self.cars):
            char = LOT_MOVING_SYMBOL if i == last_moved_index else LOT_STATIC_SYMBOL
            
            x, y = car.position
            w, h = car.size

            for pos in product(range(x, x + w), range(y, y + h)):
                grid[pos] = LOT_CAR_NAMES[i] % char
        
        return '\n'.join(
            ''.join(grid[(x, y)] for x in range(self.size.x))
            for y in range(self.size.y)
        )

    __str__ = partialmethod(format_move, -1)
