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

    pub fn get_unoccupied_squares(&self) -> Vec<(usize, usize)> {
        let mut unoccupied_squares = vec![];
        for x in 0..self.dim_x {
            for y in 0..self.dim_y {
                if self.cells[x][y].ownership == Ownership::None {
                    unoccupied_squares.push((x, y));
                }
            }
        }
        unoccupied_squares
    }

    fn get_neighbours(&self, x: isize, y: isize) -> Vec<Cell> {
        let mut neighbours: Vec<Cell> = Vec::with_capacity(8);
        let neighbours_coords: Vec<(isize, isize)> = vec![
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
            (x - 1, y - 1),
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
            None => panic!("The board is empty: x dimension is zero"),
        }
        if dim_y == 0 {
            panic!("The board is empty: y dimension is zero")
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

    pub fn check_winner(&self, player: Ownership) -> bool {
        let connected_components: Vec<Vec<Cell>> = self.find_connected_components();
        let mut found: bool;
        for connected_comp in &connected_components {
            match player {
                Ownership::Player1 => {
                    found = connected_comp
                        .iter()
                        .any(|cell: &Cell| cell.ownership == Ownership::Player1 && cell.y == 0)
                        && connected_comp.iter().any(|cell: &Cell| {
                            cell.ownership == Ownership::Player1 && cell.y == self.dim_y - 1
                        });
                }
                Ownership::Player2 => {
                    found = connected_comp
                        .iter()
                        .any(|cell: &Cell| cell.ownership == Ownership::Player2 && cell.x == 0)
                        && connected_comp.iter().any(|cell: &Cell| {
                            cell.ownership == Ownership::Player2 && cell.x == self.dim_x - 1
                        });
                }
                Ownership::None => {
                    panic!("Winner conditions can't be checked for an invalid player")
                }
            }
            if found {
                return true;
            }
        }
        false
    }

    pub fn make_move(&mut self, coords: (usize, usize), owner: Ownership) {
        self.cells[coords.0][coords.1].ownership = owner;
    }

    pub fn to_string(&self) -> String {
        let mut result = String::new();
        for _ in 0..self.dim_x * 4 {
            result.push('-');
        }
        result.push_str("\n");
        let mut offset = 0;
        for y in (0..self.dim_y).rev() {
            for _ in 0..offset {
                result.push(' ')
            }
            result.push_str("|  ");
            for x in 0..self.dim_x {
                match self.cells[x][y].ownership {
                    Ownership::Player1 => result.push('0'),
                    Ownership::Player2 => result.push('1'),
                    Ownership::None => result.push('_'),
                }
                result.push_str("  ");
            }
            result.push_str("|\n");
            offset += 2;
        }

        for _ in 0..offset {
            result.push(' ')
        }
        for _ in 0..self.dim_x * 4 {
            result.push('-');
        }
        result.push_str("\n");
        result
    }
}

#[cfg(test)]
mod tests {
    use crate::game::board::Board;
    use crate::game::cell::{Cell, Ownership};
    use rstest::*;
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
        let valid_squares: [(isize, isize); 6] = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (1, 2)];
        for (x, y) in valid_squares {
            assert!(small_board.is_valid_square(x, y));
        }
        let invalid_squares: [(isize, isize); 4] = [(2, 0), (2, 1), (2, 2), (3, 3)];
        for (x, y) in invalid_squares {
            assert!(!small_board.is_valid_square(x, y));
        }
    }

    #[test]
    fn test_get_neighbours() {
        let truth: Vec<Cell> = vec![Cell::new(1, 0), Cell::new(0, 1), Cell::new(1, 1)];
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
        let mut visited_nodes: Vec<Vec<bool>> = vec![vec![true; 4]; 2];
        visited_nodes[0][2] = false;
        assert_eq!(Board::find_next_node_to_visit(&visited_nodes), Some((0, 2)));
        let visited_nodes: Vec<Vec<bool>> = vec![vec![true, true, true, false]];
        assert_eq!(Board::find_next_node_to_visit(&visited_nodes), Some((0, 3)));
        let visited_nodes: Vec<Vec<bool>> = vec![vec![true, true]];
        assert_eq!(Board::find_next_node_to_visit(&visited_nodes), None);
    }

    /*
     ----------
     ' 1  0  2 '
      ' 0  0  2 '
       ' 0  1  0 '
         ----------
    */
    #[fixture]
    fn testing_board() -> Board {
        let mut board: Board = Board::new_from_dim(3);
        board.cells[0][2].ownership = Ownership::Player1;
        board.cells[1][0].ownership = Ownership::Player1;
        board.cells[2][1].ownership = Ownership::Player2;
        board.cells[2][2].ownership = Ownership::Player2;
        board
    }

    #[fixture]
    fn testing_visited_nodes() -> Vec<Vec<bool>> {
        vec![vec![false; 3]; 3]
    }

    #[test]
    fn test_get_neighbours_board_size_three() {
        let truth: Vec<Cell> = vec![
            Cell::new(0, 0),
            Cell::new(1, 0),
            Cell::new(0, 1),
            Cell::new(2, 1),
            Cell::new(1, 2),
            Cell::new(2, 2),
        ];
        let board: Board = Board::new_from_dim(3);
        let result = board.get_neighbours(1, 1);
        for neighbour in result {
            assert_eq!(truth.contains(&neighbour), true);
        }
    }

    #[rstest]
    fn test_expand_component_of_size_one(
        testing_board: Board,
        mut testing_visited_nodes: Vec<Vec<bool>>,
    ) {
        let starting_cell: Cell = Cell::new_from_ownership(0, 2, Ownership::Player1);
        let component: Vec<Cell> =
            testing_board.expand_component(&mut testing_visited_nodes, starting_cell);
        assert_eq!(component.len(), 1);
        assert_eq!(component[0], starting_cell);
    }

    #[rstest]
    fn test_expand_component_of_size_two(
        testing_board: Board,
        mut testing_visited_nodes: Vec<Vec<bool>>,
    ) {
        let starting_cell: Cell = Cell::new_from_ownership(2, 1, Ownership::Player2);
        testing_visited_nodes[2][1] = true;
        let component: Vec<Cell> =
            testing_board.expand_component(&mut testing_visited_nodes, starting_cell);
        assert_eq!(component.len(), 2);
        assert_eq!(component[0], starting_cell);
        assert_eq!(
            component[1],
            Cell::new_from_ownership(2, 2, Ownership::Player2)
        );
    }

    #[rstest]
    fn test_find_connected_components_in_board_size_two(testing_board: Board) {
        let connected_components: Vec<Vec<Cell>> = testing_board.find_connected_components();
        assert_eq!(connected_components.len(), 3);
        let components_truth: Vec<Vec<Cell>> = vec![
            vec![Cell::new_from_ownership(0, 2, Ownership::Player1)],
            vec![Cell::new_from_ownership(1, 0, Ownership::Player1)],
            vec![
                Cell::new_from_ownership(2, 1, Ownership::Player2),
                Cell::new_from_ownership(2, 2, Ownership::Player2),
            ],
        ];
        for component in connected_components {
            assert_eq!(components_truth.contains(&component), true);
        }
    }

    /*
     ----------
     ' 1  2  2 '
      ' 2  2  1 '
       ' 0  1  1 '
         ----------
    */
    #[fixture]
    fn testing_end_game_board() -> Board {
        let mut board: Board = Board::new_from_dim(3);
        board.cells[0][1].ownership = Ownership::Player2;
        board.cells[0][2].ownership = Ownership::Player1;
        board.cells[1][0].ownership = Ownership::Player1;
        board.cells[1][1].ownership = Ownership::Player2;
        board.cells[1][2].ownership = Ownership::Player2;
        board.cells[2][0].ownership = Ownership::Player1;
        board.cells[2][1].ownership = Ownership::Player1;
        board.cells[2][2].ownership = Ownership::Player2;
        board
    }

    #[rstest]
    #[should_panic]
    fn test_check_winner_of_invalid_player(testing_end_game_board: Board) {
        testing_end_game_board.check_winner(Ownership::None);
    }

    #[rstest]
    fn test_check_winner(testing_end_game_board: Board) {
        assert!(!testing_end_game_board.check_winner(Ownership::Player1));
        assert!(testing_end_game_board.check_winner(Ownership::Player2));
    }

    /*
     ----------
     ' 1  0  2 '
      ' 0  0  2 '
       ' 0  1  0 '
         ----------
    */
    #[rstest]
    fn test_get_unoccupied_squares(testing_board: Board) {
        let result: Vec<(usize, usize)> = testing_board.get_unoccupied_squares();
        let truth: [(usize, usize); 5] = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0)];
        assert_eq!(result.len(), 5);
        for coord in truth {
            assert_eq!(result.contains(&coord), true);
        }
    }

    /*
     ----------
     ' 2  2  1 '
      ' 1  1  1 '
       ' 0  2  2 '
         ----------
    */
    #[fixture]
    fn testing_board_no_winners() -> Board {
        let mut board: Board = Board::new_from_dim(3);
        board.cells[1][0].ownership = Ownership::Player2;
        board.cells[2][0].ownership = Ownership::Player2;
        board.cells[0][1].ownership = Ownership::Player1;
        board.cells[1][1].ownership = Ownership::Player1;
        board.cells[2][1].ownership = Ownership::Player1;
        board.cells[0][2].ownership = Ownership::Player2;
        board.cells[1][2].ownership = Ownership::Player2;
        board.cells[2][2].ownership = Ownership::Player1;
        board
    }

    #[rstest]
    fn test_find_connected_components_in_board_size_three(testing_board_no_winners: Board) {
        let connected_components: Vec<Vec<Cell>> =
            testing_board_no_winners.find_connected_components();
        assert_eq!(connected_components.len(), 3);
        let components_truth: Vec<Vec<Cell>> = vec![
            vec![
                Cell::new_from_ownership(1, 0, Ownership::Player2),
                Cell::new_from_ownership(2, 0, Ownership::Player2),
            ],
            vec![
                Cell::new_from_ownership(0, 1, Ownership::Player1),
                Cell::new_from_ownership(1, 1, Ownership::Player1),
                Cell::new_from_ownership(2, 1, Ownership::Player1),
                Cell::new_from_ownership(2, 2, Ownership::Player1),
            ],
            vec![
                Cell::new_from_ownership(0, 2, Ownership::Player2),
                Cell::new_from_ownership(1, 2, Ownership::Player2),
            ],
        ];
        for component in connected_components {
            assert_eq!(components_truth.contains(&component), true);
        }
    }

    #[rstest]
    fn test_check_winner_of_unfinished_game(testing_board_no_winners: Board) {
        assert!(!testing_board_no_winners.check_winner(Ownership::Player1));
        assert!(!testing_board_no_winners.check_winner(Ownership::Player2));
    }

    /*
     ----------
     ' 0  0  1 '
      ' 0  1  2 '
       ' 0  2  1 '
         ----------
    */
    #[fixture]
    fn testing_board_no_winners_simpler() -> Board {
        let mut board: Board = Board::new_from_dim(3);
        board.cells[1][0].ownership = Ownership::Player2;
        board.cells[2][0].ownership = Ownership::Player1;
        board.cells[1][1].ownership = Ownership::Player1;
        board.cells[2][1].ownership = Ownership::Player2;
        board.cells[2][2].ownership = Ownership::Player1;
        board
    }

    #[rstest]
    fn test_find_connected_components_in_simpler_game(testing_board_no_winners_simpler: Board) {
        let connected_components: Vec<Vec<Cell>> =
            testing_board_no_winners_simpler.find_connected_components();
        let components_truth: Vec<Vec<Cell>> = vec![
            vec![Cell::new_from_ownership(2, 0, Ownership::Player1)],
            vec![
                Cell::new_from_ownership(1, 0, Ownership::Player2),
                Cell::new_from_ownership(2, 1, Ownership::Player2),
            ],
            vec![
                Cell::new_from_ownership(1, 1, Ownership::Player1),
                Cell::new_from_ownership(2, 2, Ownership::Player1),
            ],
        ];
        assert_eq!(connected_components.len(), 3);
        for component in connected_components {
            assert_eq!(components_truth.contains(&component), true);
        }
    }

    #[rstest]
    fn test_check_winner_of_unfinished_game_simpler(testing_board_no_winners_simpler: Board) {
        assert!(!testing_board_no_winners_simpler.check_winner(Ownership::Player1));
        assert!(!testing_board_no_winners_simpler.check_winner(Ownership::Player2));
    }
}
