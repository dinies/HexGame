pub enum Ownership {
    None,
    Player1,
    Player2,
}

pub struct Cell {
    pub ownership: Ownership,
}

impl Cell {
    pub fn default() -> Self{
        Self{ownership : Ownership::None}
    }
    pub fn new() -> Self {
        Self{ownership : Ownership::None}
    }
    pub fn to_string_now(&self) {
        println!("Hello, from Cell!");
    }
}
