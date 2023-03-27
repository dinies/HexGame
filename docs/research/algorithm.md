# Introduction

The goal of this notes is to sketch the plan to get an AI to play the board game of Hex.

The baseline, which esentially we will to reimplement the "AlphaGo Zero" before experimenting with algorithms that depart from it.

AlphaGo Zero was an algorithm that learn through self-play to play go using reinforcement learning.

# Resources

- https://discovery.ucl.ac.uk/id/eprint/10045895/1/agz_unformatted_nature.pdf :the main preprint of the original AlphaGo Zero project
-https://arxiv.org/pdf/1712.01815v1.pdf the Alpha zero paper (very short!! need more info)
- https://nikcheerla.github.io/deeplearningschool/2018/01/01/AlphaZero-Explained/ : an onteresting blog post specifically on alphazero
- http://tim.hibal.org/blog/alpha-zero-how-and-why-it-works/:
A nice blog plost explaining AlphaGo Zero step by step
- https://www.deepmind.com/blog/muzero-mastering-go-chess-shogi-and-atari-without-rules  : deepmind blog post on muzero, the evolution of alphago zero that works in even more general settings without the algorith needing to know the game rules
- https://towardsdatascience.com/alphazero-chess-how-it-works-what-sets-it-apart-and-what-it-can-tell-us-4ab3d2d08867#:~:text=In%20short%2C%20AlphaZero%20is%20a,the%20rules%20of%20said%20games.%C3%B9 : blog post on alphago zero
- https://www.youtube.com/watch?v=0slFo1rV0EM: alphago zero video going over the paper
- https://youtu.be/We20YSAJZSE: muzero video going over the paper




# Notes

Here I will take notes as I read along, in order to fully understand the method used.

Just to be completelt clear the goal initially is just to reimplement Alpha Zero, the third iteration of algorithms that could play Go, chess, shogu (and most likely Hex therefore), but still had to have in its core a knoweldge of how the game works.

## Basics
- Main ingredient: a neural network  $f_{\theta}$ that takes as a input the state $s$ of the board and spits out two componets, a scalar $v$ and a vector of probabilities $\textbf{p}$ over possible actions.

- The scalar $v$ is meant to be an estimate of the expected outcome $z$ from poistion $s$ (i.e. is an approximation to the value function , in RL terms)

- Both the value estimates and move probs are learned  from self play and in terms they inform the MCTS, monte carlo tree search.

- MCTS is how AlphaZero explore the search space.

## MCTS

- Each search starts from a root $s_{root}$ until it reaches a final state 
(I thought this would take long, but it goes in a linear way, so it's okay. For example for  Hex it is at most 121 steps we are going to do to reach a final state.)

- Crucoial step: in each simulation we select in each state $s$ a move $a$ that has:
    - low visit count
    - high move prob
    - high value

    all according our current estimates given by the approximator $f_{\theta}$

- The result of a whole search (so multiple simulations) is a vector of probabilitis $\pi$ over moves. (so in a way now this is our best noisy observation of what we had first before compeltely estimated as $\mathbf{p}$ )


- Note for me: this i think a case of a EM algorithm applied to the pair $(z,\pi)$: we start with a random approximation $(v_0,p_0)$. This gives a way of pruning the search tree to get a first observaton $(z_0,\pi_0)$. This one, can then lead to a better approximation $(v_1,p_1)$, which will help gather better data to obtain a new observation point $(z_1, \pi_1)$ and so on. This remind of policy iteration, which consist of policy evaluatioona and improvement

## Training

- The parameters  $\theta$ of the deep neural network is learned through self play.

- Games are played by selecting moves for bothe players using the MCTS, with $a_t \sim \pi_t)$

    - from me: so, in each MCTS the simulations are driven implicitly by our function approximator. Finished that, for each turn we have a observed sampled policy $\pi_t$. This makes sense, but already one could think that we could use the "worse" approximation $p$. The end of a game gives rise to an observed value of $z$.

- The loss function of the networks tries to minimise the eror of $v_t$ from $z_t$ and also to maxmise the similarities of the prob vectors $p_t$ from $\pi_t$ (so this is why the cross entropy, think of the KL-divergences, see also: [here](https://stats.stackexchange.com/questions/357963/what-is-the-difference-between-cross-entropy-and-kl-divergence))

- loss function:
$$(z-v)^2-\pi^T\log p +c||\theta||^2$$


## Methods

- Most of the methods sextion in the AZ paper talks about previous methods.
- Interesting to note that for chess and shogi they called a game a draw if it did not terminate within a typical time

## Network arhcitecture

- Input is a *stack of planes*: we have $T$ sets, each having $M$ planes each with size $N \times N$

- The set T sets rapresent the board at time $t- (T-1)$ up to $t$, so we can call the hyper param T as the "lag" factors (my notation),i.e. how many previous states we want to consider to approximate value and actions


- Each of the M planes are binary feature plane such as

TODO:finish here!!