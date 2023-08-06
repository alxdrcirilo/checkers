# Checkers
[![checkers](https://github.com/alxdrcirilo/checkers/actions/workflows/coveralls.yml/badge.svg)](https://github.com/alxdrcirilo/checkers/actions/workflows/coveralls.yml)
[![coverage](https://coveralls.io/repos/github/alxdrcirilo/checkers/badge.svg?branch=main)](https://coveralls.io/github/alxdrcirilo/checkers?branch=main)
[![python version](https://img.shields.io/badge/python-3.11.4-blue)](https://www.python.org/downloads/release/python-3114/)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Checkers game with alpha-beta pruning implementation.

![](https://raw.githubusercontent.com/alxdrcirilo/checkers/main/checkers.png)

## AI
The AI makes use of the alpha-beta pruning algorithm, an optimization technique for efficient decision-making. It reduces the search space by pruning branches that won't  affect the final decision. It is particularly useful in two-player games with a large search space like checkers. The main goal of the algorithm is to reduce the number of nodes that need to be evaluated during the search process, making it more efficient and allowing deeper exploration of the game tree.

To evaluate the competitivity of the AI player (`WHITE`), 100 iterations of 100 games (per iteration) were performed at 5 different depths (i.e. `n={1, 2, 3, 4, 5}`). At depth `n=0`, the `WHITE` player makes random moves. As seen in the plot shown below, we can appreciate that the AI player starts being competitive at depth `n >= 2`, and it seems to stop improving at `n > 3`.

![](https://raw.githubusercontent.com/alxdrcirilo/checkers/main/docs/eval/plot_games_won.png)

## TODO
- [x] Add docstrings to [window.py](https://github.com/alxdrcirilo/checkers/blob/main/checkers/graphics/window.py)
- [x] Add logging (e.g. `INFO:REMOVE <PIECE>`)
- [ ] Add more unit tests
- [x] Add working alpha-beta pruning AI

## Credits
"Board Game Set - Checkers & Merels" [Game asset]. (n.d.). itch.io. Retrieved May 22, 2023, from https://mrserji.itch.io/board-game-set-checkers-merels
