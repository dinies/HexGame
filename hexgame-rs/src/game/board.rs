use super::cell::Cell;
use super::cell::Ownership;

/*
 A board is a set of exagonal cells stacked in a 2D matrix shape.
 It can be indexed similarly to a matrix with (x, y) coordinates.
 The (0,0) coordinate starts at the bottom left corner of the board.
 The x coordinate indexes horizontally (going from left to right)
 and the y vertically (going from bottom to top)
 The exagonal cells make so that the board is slanted in a
 romboidal shape. The slanting goes to the left.
 ----------
 '         '
  '         '
   '         '
     ----------
*/

#[derive(Debug)]
pub struct Board {
    pub cells: Vec<Vec<Cell>>,
}

impl Board {
    pub fn new() -> Self {
        Self {
            cells: vec![vec![]],
        }
    }

    pub fn new_from_dims(dim_x: usize, dim_y: usize) -> Self {
        let mut matrix = Vec::with_capacity(dim_x);
        for x in 0..dim_x {
            let mut column = Vec::with_capacity(dim_y);
            for y in 0..dim_y {
                column.push(Cell::new(x, y));
            }
            matrix.push(column);
        }
        Self { cells: matrix }
    }

    pub fn new_from_dim(dim: usize) -> Self {
        return Board::new_from_dims(dim, dim);
    }

    pub fn to_string_now(&self) {
        println!("Hello, from Board!");
        let c: Cell = Cell {
            x: 0,
            y: 0,
            ownership: Ownership::None,
        };
        c.to_string_now();
    }
    fn is_valid_square(self, x: isize, y: isize) -> bool {
        let num_columns: usize = self.cells.len();
        let num_rows;
        match self.cells.get(0) {
            Some(first_row) => num_rows = first_row.len(),
            None => panic!("The board is empty"),
        }
        return !(x < 0
            || y < 0
            || x >= num_columns.try_into().unwrap()
            || y >= num_rows.try_into().unwrap());
    }

    fn get_neighbours(self, x: isize, y: isize) -> Vec<Cell> {
        let mut neighbours: Vec<Cell> = Vec::with_capacity(8);
        let neighbours_coords: Vec<(isize, isize)> = vec![
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
            (x - 1, y - 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x + 1, y + 1),
        ];
        for (coord_x, coord_y) in neighbours_coords {
            let is_valid : bool =self.is_valid_square(coord_x, coord_y);
            if is_valid {
                neighbours.push(self.cells[0][0]);
            }
        }

        return neighbours;
    }
}

#[cfg(test)]
mod tests {
    use crate::game::board::Board;
    use crate::game::cell::{Cell, Ownership};
    #[test]
    fn test_board_contructor() {
        let empty_board: Board = Board::new();
        assert_eq!(empty_board.cells.len(), 1);
        assert_eq!(empty_board.cells[0].len(), 0);
        let small_board: Board = Board::new_from_dim(3);
        assert_eq!(small_board.cells.len(), 3);
        assert_eq!(small_board.cells[0].len(), 3);
        assert_eq!(small_board.cells[0][0].ownership, Ownership::None);
        let uneven_board: Board = Board::new_from_dims(3, 2);
        assert_eq!(uneven_board.cells.len(), 3);
        assert_eq!(uneven_board.cells[0].len(), 2);
    }

    #[test]
    fn test_get_neighbours() {
        let cell_1: Cell = Cell::new(1, 0);
        let cell_2: Cell = Cell::new(0, 1);
        let cell_3: Cell = Cell::new(1, 1);
        let truth: Vec<Cell> = vec![cell_1, cell_2, cell_3];
        let board: Board = Board::new_from_dim(3);
        assert_eq!(board.get_neighbours(0, 0), truth);
    }
}
