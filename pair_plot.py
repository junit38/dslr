#!/usr/bin/env python3

import sys
import pandas
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    if (len(sys.argv) == 1):
        print("scatter_plot.py: missing dataset")
    else:
        dataset = open(str(sys.argv[1]), 'r')
        df = pandas.read_csv(dataset)
        df = df.drop(columns=['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand'])
        sns.pairplot(df, hue='Hogwarts House')
        plt.show()
        dataset.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()