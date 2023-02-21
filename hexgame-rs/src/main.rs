pub mod game;
use game::game::Game;


fn main() {
    let mut game = Game::new( 3 );
    game.play();
}
