use super::board::Board;
use super::cell::Ownership;
use rand::seq::SliceRandom;
use rand::thread_rng;

#[derive(Debug)]
pub struct Agent {
    pub identity: Ownership,
}

pub trait RandomPlay {
    fn choose_next_move(&self, board: &Board) -> (usize, usize);
}

impl Agent {
    fn new(identity: Ownership) -> Self {
        Self { identity }
    }
}

impl RandomPlay for Agent {
    fn choose_next_move(&self, board: &Board) -> (usize, usize) {
        let possible_moves: Vec<(usize, usize)> = board.get_unoccupied_squares();
        if possible_moves.len() == 0 {
            panic!("there are no more possible moves to made on the board, the game should have already ended");
        }
        *possible_moves.choose(&mut thread_rng()).unwrap()
    }
}

#[derive(Debug)]
pub struct Game {
    pub board: Board,
    pub agents: [Box<Agent>; 2],
}

impl Game {
    pub fn new(dims: usize) -> Self {
        Self {
            board: Board::new_from_dim(dims),
            agents: [
                Box::new(Agent::new(Ownership::Player1)),
                Box::new(Agent::new(Ownership::Player2)),
            ],
        }
    }
    pub fn play(&mut self) {
        let mut game_ended = false;
        let max_iterations = 500;
        let mut current_iteration = 0;
        while current_iteration < max_iterations && !game_ended {
            let active_agent = current_iteration % 2;
            let selected_move: (usize, usize) =
                self.agents[active_agent].choose_next_move(&self.board);
            print!(
                "Board at iteration {}:\n{}",
                current_iteration,
                self.board.to_string()
            );
            self.board
                .make_move(selected_move, self.agents[active_agent].identity);
            println!("Selected move: {},{}", selected_move.0, selected_move.1);
            game_ended = self.board.check_winner(self.agents[active_agent].identity);
            if game_ended {
                println!("The winner is {}", active_agent);
                print!("Final board:\n{}", self.board.to_string());
            }
            current_iteration += 1;
        }
    }
}
