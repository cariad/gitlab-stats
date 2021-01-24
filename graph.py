from math import ceil
from sys import argv
from typing import Dict, List

import matplotlib.pyplot as plt


def plot(counter: Dict[int, int], format: str) -> None:
    keys: List[int] = sorted(counter.keys())
    counts: List[int] = [counter[key] for key in keys]
    plt.plot(keys, counts, format)


if __name__ == "__main__":
    round_to = 10.0

    data_file = argv[1]
    graph_file = argv[2]

    adds: Dict[int, int] = {}
    subs: Dict[int, int] = {}

    with open(data_file, "r") as stream:
        for line in stream:
            value = int(ceil(int(line) / round_to)) * int(round_to)
            counter = adds if value > 0 else subs
            if value not in counter:
                counter.update({value: 0})
            counter[value] += 1

    plot(adds, "g.")
    plot(subs, "r.")

    fig = plt.gcf()
    fig.set_size_inches(27, 15)

    plt.savefig(graph_file, bbox_inches="tight", dpi=100)
