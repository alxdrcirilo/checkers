# Checkers
[![checkers](https://github.com/alxdrcirilo/checkers/actions/workflows/coveralls.yml/badge.svg)](https://github.com/alxdrcirilo/checkers/actions/workflows/coveralls.yml)
[![coverage](https://coveralls.io/repos/github/alxdrcirilo/checkers/badge.svg?branch=main)](https://coveralls.io/github/alxdrcirilo/checkers?branch=main)
[![python version](https://img.shields.io/badge/python-3.11.4-blue)](https://www.python.org/downloads/release/python-3114/)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Checkers, a classic two-player board game, is played on an 8x8 grid where each player uses their distinct "checkers" to move diagonally, capturing opponent's pieces by jumping over them. The goal is to either capture all of the opponent's pieces or block them from making legal moves. "Kinging" occurs when a piece reaches the opponent's back row, allowing it to move both forward and backward; however, in this version, kings cannot "fly" or jump over multiple empty spaces like regular pieces.

![](https://raw.githubusercontent.com/alxdrcirilo/checkers/main/docs/images/checkers.png)

## Installation
### Setup Instructions
1. Clone the repository:  
`git clone https://github.com/alxdrcirilo/checkers.git`
2. Create a virtual environment:  
`virtualenv .venv`
3. Activate the virtual environment:  
`source .venv/bin/activate`
4. Install the required dependencies:  
`pip install -r requirements.txt`
5. Run the game:  
`python main.py`

## Running
Alternatively, if you're on Windows, you can simply download the latest executable in [Releases](https://github.com/alxdrcirilo/checkers/releases).

## AI
The AI makes use of the *alpha-beta pruning* algorithm, an optimization technique for efficient decision-making. It reduces the search space by pruning branches that won't  affect the final decision. It is particularly useful in two-player games with a large search space like checkers. The main goal of the algorithm is to reduce the number of nodes that need to be evaluated during the search process, making it more efficient and allowing deeper exploration of the game tree.

To evaluate the competitivity of the AI player (`WHITE`), 100 iterations of 100 games (per iteration) were performed at 5 different depths (i.e. `n = {1, 2, 3, 4, 5}`). At depth `n = 0`, the `WHITE` player makes random moves. As seen in the plot shown below, we can appreciate that the AI player starts being competitive at depth `n >= 2`, and it seems to stop improving at `n > 3`.

![](https://raw.githubusercontent.com/alxdrcirilo/checkers/main/docs/eval/plot_games_won.png)

## Notes
The `BLACK` player always starts first and is the human player. The `WHITE` player starts second and is the AI player.

## Credits
### Assets
"Board Game Set - Checkers & Merels" [Game asset]. (n.d.). itch.io. Retrieved May 22, 2023, from https://mrserji.itch.io/board-game-set-checkers-merels

### Fonts
This project uses the [Open Sans](https://fonts.google.com/specimen/Open+Sans) font.
