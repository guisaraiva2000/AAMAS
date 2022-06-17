import argparse
import numpy as np
from clean_waters import CleanWaters
from utils.analytics import compare_results
from utils.settings import MAX_STEPS

drone_types = [
    "Random",
    "Greedy",
    "Greedy w/ S. Convention",
    "Greedy w/ Roles"
]

# (title, metric)
studies = [
    ("Average Oil Spill Active Time-Steps",               "time-steps"),
    ("Average Number of Ocean Squares p/ Time-Step (%)",  "number of ocean squares / time-step (%)"),
    ("Total Number of Cleaned Squares",                   "number of squares"),
    ("Total Number of Squares Left to Clean (%)",         "number of squares (%)"),
    ("Total Number of Oil Spills",                        "number of oil spills"),
    ("Total Time-Steps Until End of Simulation",          "time-steps")
]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int)
    opt = parser.parse_args()

    if opt.episodes:
        results = {study: {drone_type: np.zeros(opt.episodes) for drone_type in drone_types} for study in studies}

        for drone_type in drone_types:
            for episode in range(opt.episodes):
                cw = CleanWaters()
                cw.initiate()
                cw.drone_chosen(drone_type)
                cw.main_loop()
                results[studies[0]][drone_type][episode] = cw.avg_oil_active_time
                results[studies[1]][drone_type][episode] = cw.avg_squares_w_ocean * 100 / MAX_STEPS
                results[studies[2]][drone_type][episode] = cw.total_cleaned_squares
                results[studies[3]][drone_type][episode] = cw.oil_left * 100 / MAX_STEPS
                results[studies[4]][drone_type][episode] = cw.total_oil_spill
                results[studies[5]][drone_type][episode] = cw.step_counter

        for study, result in results.items():
            compare_results(
                result,
                title=study[0],
                metric=study[1],
                colors=["orange", "green", "blue", "red"]
            )
    else:
        cw = CleanWaters()
        while cw.running:
            cw.initiate()
            cw.main_loop()
            cw.drone_not_chosen = True
            while cw.drone_not_chosen:
                cw.check_events()
            cw = CleanWaters()
