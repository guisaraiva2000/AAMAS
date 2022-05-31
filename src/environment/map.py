R = "recharger"
O = "ocean"

sim_map = [
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [R], [R], [R], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]],
    [[O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O], [O]]
]
