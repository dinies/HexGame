use crate::game::board::Board;
pub mod game;

fn main() {
    println!("Hello, world!");
    let b: Board = Board::new();
    b.to_string_now();
}
