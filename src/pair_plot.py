import os
import sys
import matplotlib.pyplot as plt
from constants import HOUSES, HOUSES_COLOR, COURSES
from utils import read_csv_split_houses, histogram, scatter_plot


def parse_arguments() -> str:
    """
    Parse the command-line arguments and return the path to the dataset.
    """
    if len(sys.argv) != 2 or os.path.isfile(sys.argv[1]) is False:
        print("Wrong arg : expected 'python describe.py [filename]'")
        sys.exit(1)
    else :
        return sys.argv[1]


def build_pair_plot(data: dict) -> None:
    """
    Build and display the pair plot of the courses for each house.
    """
    n = len(COURSES)
    fig, axes = plt.subplots(n, n, figsize=(n * 1.6, n * 1.6))

    for i in range(n):
        for j in range(n):
            ax = axes[i, j]
            if i == j:
                histogram(data, COURSES[i], ax)
            else:
                scatter_plot(data, COURSES[i], COURSES[j], ax)

            if i == n - 1:
                ax.set_xlabel(COURSES[j], rotation=45, ha="right", fontsize=9)
            else:
                ax.set_xticks([])

            if j == 0:
                ax.set_ylabel(COURSES[i], rotation=0, ha="right", fontsize=9)
            else:
                ax.set_yticks([])

            ax.tick_params(axis="both", labelsize=7)

    # Add legend
    legend_handles = [
        plt.Line2D(
            [],
            [],
            marker="o",
            color="w",
            label=house,
            markerfacecolor=HOUSES_COLOR[house],
            markersize=7,
            alpha=0.6,
        )
        for house in HOUSES
    ]
    fig.legend(handles=legend_handles, loc="center right", bbox_to_anchor=(1, 0.5))
    fig.suptitle("Pair Plot des Matières", fontsize=16)
    plt.subplots_adjust(
        hspace=0.2, wspace=0.2, top=0.95, bottom=0.21, left=0.15, right=0.9
    )
    plt.show()


if __name__ == "__main__":
    file_path = parse_arguments()
    data = read_csv_split_houses(file_path)
    build_pair_plot(data)
