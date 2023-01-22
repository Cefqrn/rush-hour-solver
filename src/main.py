from vector2 import Vector2
from lot import Car, Lot, Orientation, Direction


if __name__ == "__main__":
    lot = Lot(
        (
            Car(Orientation.HORIZONTAL, Vector2(2, 2), Vector2(2, 1)), # main car

            Car(Orientation.HORIZONTAL, Vector2(0, 0), Vector2(3, 1)),
            Car(Orientation.HORIZONTAL, Vector2(1, 1), Vector2(2, 1)),
            Car(Orientation.HORIZONTAL, Vector2(0, 3), Vector2(2, 1)),
            Car(Orientation.HORIZONTAL, Vector2(4, 4), Vector2(2, 1)),
            Car(Orientation.HORIZONTAL, Vector2(2, 5), Vector2(2, 1)),
            Car(Orientation.HORIZONTAL, Vector2(4, 5), Vector2(2, 1)),
            Car(Orientation.VERTICAL,   Vector2(3, 0), Vector2(1, 2)),
            Car(Orientation.VERTICAL,   Vector2(4, 0), Vector2(1, 3)),
            Car(Orientation.VERTICAL,   Vector2(5, 0), Vector2(1, 3)),
            Car(Orientation.VERTICAL,   Vector2(0, 1), Vector2(1, 2)),
            Car(Orientation.VERTICAL,   Vector2(2, 3), Vector2(1, 2)),
            Car(Orientation.VERTICAL,   Vector2(1, 4), Vector2(1, 2)),
        ),
        Vector2(6, 6),
        Direction.POSITIVE
    )

    solution = lot.solve()
    lot.print_solution(solution)
