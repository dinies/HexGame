#[derive(Debug, Clone, PartialEq)]
pub enum Ownership {
    None,
    Player1,
    Player2,
}

#[derive(Debug, Clone)]
pub struct Cell {
    pub ownership: Ownership,
}

impl Cell {
    pub fn new() -> Self {
        Self {
            ownership: Ownership::None,
        }
    }
    pub fn to_string_now(&self) {
        println!("Hello, from Cell!");
    }
}

#[cfg(test)]
mod tests {
    use crate::game::cell::Cell;
    use crate::game::cell::Ownership;
    #[test]
    fn cell_constructor() {
        let c: Cell = Cell::new();
        assert_eq!(c.ownership, Ownership::None);
    }
}
