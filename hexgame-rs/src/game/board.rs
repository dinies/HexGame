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
    pub dim_x: usize,
    pub dim_y: usize,
    pub cells: Vec<Vec<Cell>>,
}

impl Board {
    pub fn new() -> Self {
        Self {
            dim_x: 0,
            dim_y: 0,
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
        Self {
            dim_x,
            dim_y,
            cells: matrix,
        }
    }

    pub fn new_from_dim(dim: usize) -> Self {
        return Board::new_from_dims(dim, dim);
    }

    fn is_empty(&self) -> bool {
        self.dim_x == 0 || self.dim_y == 0
    }

    fn is_valid_square(&self, x: isize, y: isize) -> bool {
        if self.is_empty() {
            panic!("The board is empty")
        }
        return !(x < 0
            || y < 0
            || x >= self.dim_x.try_into().unwrap()
            || y >= self.dim_y.try_into().unwrap());
    }

    fn get_neighbours(&self, x: isize, y: isize) -> Vec<Cell> {
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
            if self.is_valid_square(coord_x, coord_y) {
                neighbours.push(
                    self.cells[usize::try_from(coord_x).unwrap()]
                        [usize::try_from(coord_y).unwrap()],
                );
            }
        }
        return neighbours;
    }

    fn find_next_node_to_visit(visited_nodes: &Vec<Vec<bool>>) -> Option<(usize, usize)> {
        let dim_x: usize = visited_nodes.len();
        let dim_y;
        match visited_nodes.get(0) {
            Some(row) => dim_y = row.len(),
            None => panic!("The board is empty"),
        }
        for x in 0..dim_x {
            for y in 0..dim_y {
                if !visited_nodes[x][y] {
                    return Some((x, y));
                }
            }
        }
        None
    }

    fn find_connected_components(&self) -> Vec<Vec<Cell>> {
        if self.is_empty() {
            return Vec::new();
        }
        let mut connected_components: Vec<Vec<Cell>> = Vec::new();
        let mut visited_nodes: Vec<Vec<bool>> = vec![vec![false; self.dim_y]; self.dim_x];

        let mut every_node_visited: bool = false;
        while !every_node_visited {
            match Self::find_next_node_to_visit(&visited_nodes) {
                Some((x, y)) => {
                    let node: Cell = self.cells[x][y];
                    visited_nodes[x][y] = true;
                    if node.ownership != Ownership::None {
                        connected_components
                            .push(self.expand_component(&mut visited_nodes, self.cells[x][y]));
                    }
                }
                None => every_node_visited = true,
            }
        }
        connected_components
    }

    fn expand_component_rec(
        &self,
        component_nodes: &mut Vec<Cell>,
        visited_nodes: &mut Vec<Vec<bool>>,
    ) {
        let node: Cell = component_nodes.last().cloned().unwrap();
        match self
            .get_neighbours(node.x.try_into().unwrap(), node.y.try_into().unwrap())
            .as_slice()
        {
            [] => (),
            neighbours => {
                for &neighbour in neighbours {
                    if !visited_nodes[neighbour.x][neighbour.y]
                        && neighbour.ownership == node.ownership
                    {
                        visited_nodes[neighbour.x][neighbour.y] = true;
                        component_nodes.push(neighbour);
                        self.expand_component_rec(component_nodes, visited_nodes);
                    }
                }
            }
        }
    }

    fn expand_component(&self, visited_nodes: &mut Vec<Vec<bool>>, node: Cell) -> Vec<Cell> {
        let mut component_nodes: Vec<Cell> = vec![node];
        self.expand_component_rec(&mut component_nodes, visited_nodes);
        component_nodes
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
    fn test_is_empty() {
        let empty_board: Board = Board::new();
        let small_board: Board = Board::new_from_dim(1);
        assert!(empty_board.is_empty());
        assert!(!small_board.is_empty());
    }

    #[test]
    #[should_panic]
    fn test_is_valid_square_on_empty_board() {
        let empty_board: Board = Board::new();
        empty_board.is_valid_square(0, 0);
    }

    #[test]
    fn test_is_valid_square_on_small_board() {
        let small_board: Board = Board::new_from_dims(2, 3);
        assert!(small_board.is_valid_square(0, 0));
        assert!(small_board.is_valid_square(0, 1));
        assert!(small_board.is_valid_square(1, 0));
        assert!(small_board.is_valid_square(1, 1));
        assert!(small_board.is_valid_square(0, 2));
        assert!(small_board.is_valid_square(1, 2));
        assert!(!small_board.is_valid_square(2, 0));
        assert!(!small_board.is_valid_square(2, 1));
        assert!(!small_board.is_valid_square(2, 2));
        assert!(!small_board.is_valid_square(3, 3));
    }

    #[test]
    fn test_get_neighbours() {
        let cell_1: Cell = Cell::new(1, 0);
        let cell_2: Cell = Cell::new(0, 1);
        let cell_3: Cell = Cell::new(1, 1);
        let truth: Vec<Cell> = vec![cell_1, cell_2, cell_3];
        let board: Board = Board::new_from_dim(2);
        assert_eq!(board.get_neighbours(0, 0), truth);
    }

    #[test]
    #[should_panic]
    fn test_find_next_node_to_visit_in_empty_board() {
        let visited_nodes: Vec<Vec<bool>> = vec![vec![false; 0]; 2];
        Board::find_next_node_to_visit(&visited_nodes);
    }

    #[test]
    fn test_find_next_node_to_visit() {

        let mut visited_nodes: Vec<Vec<bool>> = vec![vec![false; 4]; 2];
        visited_nodes[0][2] = true;
        assert_eq!( Board::find_next_node_to_visit(&visited_nodes), Some( (0,2) ));


        let visited_nodes: Vec<Vec<bool>> = 
            vec![
                vec![ true, true, true, false ],
                vec![ false , true, true, false ],
                vec![ true, true, true, false ]
            ];
        assert_eq!( Board::find_next_node_to_visit(&visited_nodes), Some( (3,0) ));
        let visited_nodes: Vec<Vec<bool>> = 
            vec![
                vec![ false, false ]
            ];
        assert_eq!( Board::find_next_node_to_visit(&visited_nodes), None );
    }
}
