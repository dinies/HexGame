#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Ownership {
    None,
    Player1,
    Player2,
}

#[derive(Debug, Clone, Copy)]
pub struct Cell {
    pub x: usize,
    pub y: usize,
    pub ownership: Ownership,
}

impl Cell {
    pub fn new(x: usize, y: usize) -> Self {
        Self {
            x,
            y,
            ownership: Ownership::None,
        }
    }
    pub fn new_from_ownership(x: usize, y: usize, ownership: Ownership) -> Self {
        Self { x, y, ownership }
    }
}

impl PartialEq for Cell {
    fn eq(&self, other: &Cell) -> bool {
        self.x == other.x && self.y == other.y && self.ownership == other.ownership
    }
}

#[cfg(test)]
mod tests {
    use crate::game::cell::Cell;
    use crate::game::cell::Ownership;
    #[test]
    fn test_cell_constructor() {
        let c: Cell = Cell::new(0, 1);
        assert_eq!(c.x, 0);
        assert_eq!(c.y, 1);
        assert_eq!(c.ownership, Ownership::None);
    }
    #[test]
    fn test_cell_constructor_from_ownership() {
        let c: Cell = Cell::new_from_ownership(0, 1, Ownership::Player1);
        assert_eq!(c.x, 0);
        assert_eq!(c.y, 1);
        assert_eq!(c.ownership, Ownership::Player1);
    }

    #[test]
    fn test_equals(){
        let c_1: Cell = Cell::new_from_ownership(0, 1, Ownership::Player1);
        let mut c_2: Cell = Cell::new(0,1);
        assert_ne!(c_1, c_2);
        c_2.ownership = Ownership::Player1;
        assert_eq!(c_1, c_2);
    }
}
