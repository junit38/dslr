#!/usr/bin/env python3

import sys
import pandas
import matplotlib.pyplot as plt


class Feature:
    name = ""
    min = 0
    max = 0
    data_max = 0
    data_ravenclaw = []
    data_gryffindor = []
    data_slytherin = []
    data_hufflepuff = []
    hist_ravenclaw = []
    hist_gryffindor = []
    hist_slytherin = []
    hist_hufflepuff = []
    data = {}

    def __init__(self, name):
        self.name = name


def print_histogram(features):
    index = 0
    for feature in features:
        if index > 5:
            while (len(feature.data_gryffindor) > feature.data_max):
                feature.data_max = len(feature.data_gryffindor)
            while (len(feature.data_ravenclaw) > feature.data_max):
                feature.data_max = len(feature.data_ravenclaw)
            while (len(feature.data_slytherin) > feature.data_max):
                feature.data_max = len(feature.data_slytherin)
            while (len(feature.data_hufflepuff) > feature.data_max):
                feature.data_max = len(feature.data_hufflepuff)
        index = index + 1
    index = 0
    for feature in features:
        if index > 5:
            while (len(feature.data_gryffindor) < feature.data_max):
                feature.data_gryffindor.append(float('NaN'))
            while (len(feature.data_hufflepuff) < feature.data_max):
                feature.data_hufflepuff.append(float('NaN'))
            while (len(feature.data_ravenclaw) < feature.data_max):
                feature.data_ravenclaw.append(float('NaN'))
            while (len(feature.data_slytherin) < feature.data_max):
                feature.data_slytherin.append(float('NaN'))
        index = index + 1
    index = 0
    for feature in features:
        if index > 5:
            feature.data.update({"Ravenclaw": feature.data_ravenclaw})
            feature.data.update({"Gryffindor": feature.data_gryffindor})
            feature.data.update({"Slytherin": feature.data_slytherin})
            feature.data.update({"Hufflepuff": feature.data_hufflepuff})
            df = pandas.DataFrame(feature.data, columns=['Hufflepuff', 'Ravenclaw', 'Gryffindor', 'Slytherin'])
            df.plot.hist(bins=20, title=feature.name)
        index = index + 1
    plt.show()


def set_data(features, lines):
    for line in lines:
        data = line.split(',')
        index = 0
        house = ""
        for value in data:
            if (index == 1):
                house = value
            if (index > 5 and value):
                if (features[index].min > float(value)):
                    features[index].min = float(value)
                if (features[index].max < float(value)):
                    features[index].max = float(value)
                if (house == "Ravenclaw"):
                    if (len(features[index].data_ravenclaw) == 0):
                        features[index].data_ravenclaw = [float(value)]
                    else:
                        features[index].data_ravenclaw.append(float(value))
                if (house == "Gryffindor"):
                    if (len(features[index].data_gryffindor) == 0):
                        features[index].data_gryffindor = [float(value)]
                    else:
                        features[index].data_gryffindor.append(float(value))
                if (house == "Slytherin"):
                    if (len(features[index].data_slytherin) == 0):
                        features[index].data_slytherin = [float(value)]
                    else:
                        features[index].data_slytherin.append(float(value))
                if (house == "Hufflepuff"):
                    if (len(features[index].data_hufflepuff) == 0):
                        features[index].data_hufflepuff = [float(value)]
                    else:
                        features[index].data_hufflepuff.append(float(value))
            index = index + 1


def histogram(headers, lines):
    features = []
    for header in headers:
        feature = Feature(header)
        features.append(feature)
    set_data(features, lines)
    print_histogram(features)


def main():
    if (len(sys.argv) == 1):
        print("histogram.py: missing dataset")
    else:
        dataset = open(str(sys.argv[1]), 'r')
        headers = dataset.readline().split(',')
        lines = dataset.readlines()
        histogram(headers, lines)
        dataset.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()