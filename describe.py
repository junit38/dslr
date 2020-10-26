#!/usr/bin/env python3

import sys
import pandas
import math


class Feature:
    name = ""
    count = 0
    min = float('NaN')
    max = float('NaN')
    mean = 0
    mean_total = 0
    variance = 0
    variance_total = 0
    data = []
    first_quartile_index = 0
    second_quartile_index = 0
    third_quartile_index = 0
    first_quartile = 0
    second_quartile = 0
    third_quartile = 0

    def __init__(self, name):
        self.name = name


def print_features(features):
    data = {}
    index = 0
    for feature in features:
        if (index > 5):
            data.update({feature.name: [feature.count, feature.mean,
                feature.std, feature.min, feature.first_quartile,
                feature.second_quartile, feature.third_quartile, feature.max]})
        index = index + 1
    df = pandas.DataFrame(data, index=['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max'])
    print(df.to_markdown())


def set_data(features, lines):
    # count min max mean and data
    for line in lines:
        data = line.split(',')
        index = 0
        for value in data:
            if (index > 5 and value):
                features[index].count = features[index].count + 1
                features[index].mean_total = features[index].mean_total + float(value)
                if (math.isnan(features[index].min)):
                    features[index].min = float(value)
                if (math.isnan(features[index].max)):
                    features[index].max = float(value)
                if (features[index].min > float(value)):
                    features[index].min = float(value)
                if (features[index].max < float(value)):
                    features[index].max = float(value)
                if (len(features[index].data) == 0):
                    features[index].data = [float(value)]
                else:
                    features[index].data.append(float(value))
            index = index + 1
    # mean
    for feature in features:
        if feature.count != 0:
            feature.mean = feature.mean_total / feature.count
    # variance
    for line in lines:
        data = line.split(',')
        index = 0
        for value in data:
            if (index > 5 and value):
                diff = float(value) - features[index].mean
                features[index].variance_total = features[index].variance_total + pow(diff, 2)
            index = index + 1
    # std
    for feature in features:
        if feature.count != 0:
            feature.variance = feature.variance_total / feature.count
            feature.std = math.sqrt(feature.variance)
    # quartiles index
    for feature in features:
        if feature.mean != 0:
            feature.first_quartile_index = feature.count / 4
            feature.second_quartile_index = (feature.count / 4) * 2
            feature.third_quartile_index = (feature.count / 4) * 3
    # quartile
    last = 0
    for feature in features:
        index = 0
        feature.data.sort()
        for value in feature.data:
            if (index == feature.first_quartile_index):
                feature.first_quartile = value
            if (index == feature.second_quartile_index):
                feature.second_quartile = value
            if (index == feature.third_quartile_index):
                feature.third_quartile = value
            if (index > feature.first_quartile_index and feature.first_quartile == 0):
                feature.first_quartile = (value + last) / 2
            if (index > feature.second_quartile_index and feature.second_quartile == 0):
                feature.second_quartile = (value + last) / 2
            if (index > feature.third_quartile_index and feature.third_quartile == 0):
                feature.third_quartile = (value + last) / 2
            last = value
            index = index + 1

def describe(headers, lines):
    features = []
    for header in headers:
        feature = Feature(header)
        features.append(feature)
    set_data(features, lines)
    print_features(features)


def main():
    if (len(sys.argv) == 1):
        print("describe.py: missing dataset")
    else:
        dataset = open(str(sys.argv[1]), 'r')
        headers = dataset.readline().split(',')
        lines = dataset.readlines()
        describe(headers, lines)
        dataset.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()