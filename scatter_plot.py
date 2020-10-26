#!/usr/bin/env python3

import sys
import pandas
import matplotlib.pyplot as plt

def main():
    if (len(sys.argv) == 1):
        print("scatter_plot.py: missing dataset")
    else:
        dataset = open(str(sys.argv[1]), 'r')
        df = pandas.read_csv(dataset)
        fig, ax = plt.subplots()
        # for raw in df:
        #     for raw2 in df:
        #         scatter_plot = plt.scatter(df[raw], df[raw2])
        #         ax.set_xlabel(raw)
        #         ax.set_ylabel(raw2)
        #         plt.show()
        scatter_plot = plt.scatter(df["Astronomy"], df["Defense Against the Dark Arts"])
        ax.set_xlabel("Astronomy")
        ax.set_ylabel("Defense Against the Dark Arts")
        plt.show()
        dataset.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()