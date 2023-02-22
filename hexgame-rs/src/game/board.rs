use crate::game::cell::Cell;
use crate::game::cell::Ownership;

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
pub struct Board{
    pub cells: Vec<Vec<Cell>>
    
}

impl Board{
    
    pub fn new() -> Self {
        Self{cells : vec![vec![]]}
    }

    pub fn new_from_dim( dim: usize ) -> Self{
        Self{cells : vec![vec![Cell::new();dim];dim]}
    }

    pub fn new_from_dims( dim_x: usize, dim_y: usize ) -> Self{
        Self{cells : vec![vec![Cell::new();dim_y];dim_x]}
    }

    pub fn to_string_now(&self) {
        println!("Hello, from Board!");
        let c: Cell = Cell{ownership : Ownership::None};
        c.to_string_now();
    }
}
