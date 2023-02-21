use crate::game::cell::Cell;
use crate::game::cell::Ownership;

pub struct Board{
    
}

impl Board{

    pub fn to_string_now(&self) {
        println!("Hello, from Board!");
        let c: Cell = Cell{ownership : Ownership::None};
        c.to_string_now();
    }
}
