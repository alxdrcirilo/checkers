import time
from multiprocessing.pool import Pool

import pandas as pd
import tqdm

from checkers.ai.arena import Arena


def task(iterable):
    start_time = time.time()
    depth, iteration = iterable
    checkers = Arena()
    black_wins, white_wins = checkers.play(games=100, depth=depth)
    end_time = time.time()
    run_time = (end_time - start_time) / 60
    return [depth, iteration, f"{run_time:.2f}", black_wins, white_wins]


def main():
    header = ["depth", "iteration", "runtime", "BLACK", "WHITE"]
    df = pd.DataFrame(columns=header)
    replicates = 100

    with Pool(8) as pool:
        for depth in range(7):
            print(f"{depth=}")
            for result in tqdm.tqdm(
                pool.imap(task, list(zip([depth] * replicates, range(replicates)))),
                total=replicates,
            ):
                df.loc[len(df.shape[0]) + 1] = result  # type: ignore

    df.to_csv(path_or_buf="results.csv", index=False)


if __name__ == "__main__":
    main()
