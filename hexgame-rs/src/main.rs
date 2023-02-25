pub mod game;

fn main() {
    println!("Hello, world!");
    let b: game::board::Board = game::board::Board::new();
    b.to_string_now();
}
