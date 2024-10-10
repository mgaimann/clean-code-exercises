# The `RasterGrid` represents a structured, rectangular grid in 2d space.
# Each cell of the grid is identified by its column/row index pair:
#
#  ________ ________ ________
# |        |        |        |
# | (0, 1) | (1, 1) | (2, 2) |
# |________|________|________|
# |        |        |        |
# | (0, 0) | (1, 0) | (2, 0) |
# |________|________|________|
#
#
# One can construct a `RasterGrid` by specifying the lower left and upper right
# corners of a domain and the number of cells one wants to use in x- and y-directions.
# Then, `RasterGrid` allows to iterate over all cells and retrieve the center point
# of that cell.
#
# This class can be significantly cleaned up, though. Give it a try, and if you need
# help you may look into the file `raster_grid_hints.py`.
# Make sure to make small changes, verifying that the test still passes, and put
# each small change into a separate commit.
from typing import Tuple
from math import isclose
from dataclasses import dataclass

@dataclass
class Rectangle:
    x_lower_left: float
    y_lower_left: float
    x_upper_right: float
    y_upper_right: float

class RasterGrid:
    @dataclass
    class Cell:
        idx_x: int
        idx_y: int

    def __init__(self,
                 box: Rectangle,
                 n_cells_x: int,
                 n_cells_y: int) -> None:

        self.box = box
        self._n_cells_x = n_cells_x
        self._n_cells_y = n_cells_y
        self.n_cells = n_cells_x * n_cells_y
        self.cells = [
            self.Cell(i, j) for i in range(n_cells_x) for j in range(n_cells_y)
        ]

    def get_cell_center(self, cell: Cell) -> Tuple[float, float]:
        return (
            self.box.x_lower_left + (float(cell.idx_x) + 0.5) * (self.box.x_upper_right - self.box.x_lower_left) / self._n_cells_x,
            self.box.y_lower_left + (float(cell.idx_y) + 0.5) * (self.box.y_upper_right - self.box.y_lower_left) / self._n_cells_y
        )


def test_number_of_cells():
    x0 = 0.0
    y0 = 0.0
    dx = 1.0
    dy = 1.0
    box = Rectangle(x0, y0, x0 + dx, y0 + dy)
    assert RasterGrid(box, 10, 10).n_cells == 100
    assert RasterGrid(box, 10, 20).n_cells == 200
    assert RasterGrid(box, 20, 10).n_cells == 200
    assert RasterGrid(box, 20, 20).n_cells == 400


def test_cell_center():
    box = Rectangle(0.0, 0.0, 2.0, 2.0)
    grid = RasterGrid(box, 2, 2)
    expected_centers = [
        (0.5, 0.5),
        (1.5, 0.5),
        (0.5, 1.5),
        (1.5, 1.5)
    ]

    for cell in grid.cells:
        for center in expected_centers:
            if isclose(grid.get_cell_center(cell)[0], center[0]) and isclose(grid.get_cell_center(cell)[1], center[1]):
                expected_centers.remove(center)

    assert len(expected_centers) == 0


if __name__ == "__main__":
    test_number_of_cells()
    test_cell_center()
    print("All tests passed")
