import argparse

import numpy as np

from clean_waters import CleanWaters
from utils.analytics import compare_results

N_RUNS = 2
drone_types = ["Random", "Greedy", "Greedy w/ S. Convention", "Greedy w/ Roles"]
studies = ["Average time spent cleaning an oil spill"]  # , "Average number of cleaned squares per step"]
avg_oil_clean_time = []

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=-1)
    opt = parser.parse_args()

    if opt.episodes != -1:
        runs_counter = 0
        results = {studies[0]: {}}

        for drone_type in drone_types:
            cw = CleanWaters()
            while cw.running:
                runs_counter += 1
                cw.initiate()
                cw.drone_chosen(drone_type)
                cw.main_loop()
                res = np.zeros(1)
                res[0] = cw.avg_oil_clean_time
                results[studies[0]][drone_type] = res
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
            #break
