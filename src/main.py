import argparse

import numpy as np

from clean_waters import CleanWaters
from utils.analytics import compare_results

drone_types = [
    "Random",
    "Greedy",
    "Greedy w/ S. Convention",
    "Greedy w/ Roles"
]

studies = [
    "Average time spent cleaning an oil spill",
    "Average number of clean squares per step",
    "Total number of cleaned squares",
    "Total number of squares left to clean",
    "Total number of oil spills"
]


def get_res(episodes, metric):
    res = np.zeros(episodes)
    res[0] = metric
    return res


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=-1)
    opt = parser.parse_args()

    if opt.episodes != -1:
        runs_counter = 0
        results = {study: {} for study in studies}

        for drone_type in drone_types:
            cw = CleanWaters()
            while cw.running:
                cw.initiate()
                cw.drone_chosen(drone_type)
                cw.main_loop()
                results[studies[0]][drone_type] = get_res(1, cw.avg_oil_active_time)
                results[studies[1]][drone_type] = get_res(1, cw.avg_tiles_w_ocean)
                results[studies[2]][drone_type] = get_res(1, cw.total_cleaned_tiles)
                results[studies[3]][drone_type] = get_res(1, cw.oil_left)
                results[studies[4]][drone_type] = get_res(1, cw.total_oil_spill)
                break

        for study, result in results.items():
            compare_results(
                result,
                title=study,
                metric=study,
                colors=["orange", "green", "blue", "red"]
            )
    else:
        cw = CleanWaters()
        while cw.running:
            cw.initiate()
            cw.main_loop()
            cw = CleanWaters()
