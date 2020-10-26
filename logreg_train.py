#!/usr/bin/env python3

import sys
import pandas
import math

class House:
    name = ""
    minx1 = float('NaN')
    maxx1 = float('NaN')
    minx2 = float('NaN')
    maxx2 = float('NaN')
    datasetx1 = []
    datasetx2 = []
    theta0 = 0
    theta1 = 1
    theta2 = 1

    def __init__(self, name):
        self.name = name

    def getHx(self, x1, x2):
    	cal = self.theta0 + self.theta1 * self.getnormalizedvalx1(x1) + self.theta2 * self.getnormalizedvalx2(x2)
    	return 1 / (1 + math.exp(cal))

    def getnormalizedvalx1(self, x):
    	normalize_val = (x - self.minx1) / (self.maxx1 - self.minx1)
    	return normalize_val

    def getnormalizedvalx2(self, x):
    	normalize_val = (x - self.minx2) / (self.maxx2 - self.minx2)
    	return normalize_val

    def getx(self, x1, x2):
    	cal = self.theta0 + self.theta1 * self.getnormalizedvalx1(x1) + self.theta2 * self.getnormalizedvalx2(x2)
    	return cal

def setminmax(house):
	for value in house.datasetx1:
		if math.isnan(house.minx1):
			house.minx1 = value
		if math.isnan(house.maxx1):
			house.maxx1 = value
		if (house.minx1 < value):
			house.minx1 = value
		if (house.maxx1 > value):
			house.maxx1 = value
	for value in house.datasetx2:
		if math.isnan(house.minx2):
			house.minx2 = value
		if math.isnan(house.maxx2):
			house.maxx2 = value
		if (house.minx2 < value):
			house.minx2 = value
		if (house.maxx2 > value):
			house.maxx2 = value


def setcount(house):
	count = 0
	for value in house.houses:
		count = count + 1
	house.count = count


def getcostfunction(house):
	index = 0
	sumtotal = 0
	while (index < 1600):
		if not (math.isnan(house.datasetx1[index]) or math.isnan(house.datasetx2[index])):
			hx = house.getHx(house.datasetx1[index], house.datasetx2[index])
			if (house.houses[index] == house.name):
				y = 1
			else:
				y = 0
			if (not math.isnan(hx) and hx > 0):
				if y == 1:
					sumtotal += y * math.log(hx)
				else:
					sumtotal += math.log(1 - hx)
				# sumtotal += y * math.log(hx) + (1 - y) * math.log(1 - hx)
		index = index + 1
	cost = - sumtotal / 1600
	return cost

def getderivetheta0(house, lr):
	index = 0
	sumtotal = 0
	while (index < 1600):
		hx = house.getHx(house.datasetx1[index], house.datasetx2[index])
		if (house.houses[index] == house.name):
			y = 1
		else:
			y = 0
		if (not math.isnan(hx) and hx > 0):
			sumtotal += ((hx - y) * 1)
		index = index + 1
	derive = sumtotal * (lr / 1600)
	return derive


def getderivetheta1(house, lr):
	index = 0
	sumtotal = 0
	while (index < 1600):
		hx = house.getHx(house.datasetx1[index], house.datasetx2[index])
		if (house.houses[index] == house.name):
			y = 1
		else:
			y = 0
		if (not math.isnan(hx) and hx > 0):
			sumtotal += ((hx - y) * house.getnormalizedvalx1(house.datasetx1[index]))
		index = index + 1
	derive = sumtotal * (lr / 1600)
	return derive

def getderivetheta2(house, lr):
	index = 0
	sumtotal = 0
	while (index < 1600):
		hx = house.getHx(house.datasetx1[index], house.datasetx2[index])
		if (house.houses[index] == house.name):
			y = 1
		else:
			y = 0
		if (not math.isnan(hx) and hx > 0):
			sumtotal += ((hx - y) * house.getnormalizedvalx2(house.datasetx2[index]))
		index = index + 1
	derive = sumtotal * (lr / 1600)
	return derive


def train(house):
	oldcost = 0
	lr = 10
	diff = 1
	while (abs(diff) > 0.0001):
		cost = getcostfunction(house)
		if (cost - oldcost > 0):
			lr = lr * - 1
		house.theta0 = house.theta0 - getderivetheta0(house, lr)
		house.theta1 = house.theta1 - getderivetheta1(house, lr)
		house.theta2 = house.theta2 - getderivetheta2(house, lr)
		print("house.theta0", house.theta0)
		print("house.theta1", house.theta1)
		print("house.theta2", house.theta2)
		print("cost", getcostfunction(house))
		diff = cost - oldcost
		oldcost = cost


def prepare(df):
	model = open("model", 'w')
	house = House("Gryffindor")
	house.datasetx1 = df["Herbology"]
	house.datasetx2 = df["Flying"]
	house.houses = df["Hogwarts House"]
	setminmax(house)
	setcount(house)
	iteration = 0
	print("Training Gryffindor")
	diff = 1
	while (abs(diff) > 0.0001):
		print("Iteration " + str(iteration))
		oldcost = getcostfunction(house)
		train(house)
		diff = oldcost - getcostfunction(house)
		iteration = iteration + 1
	model.write(str(house.theta0) + "," + str(house.theta1) + "," + str(house.theta2) + "\n")
	house = House("Ravenclaw")
	house.datasetx1 = df["Flying"]
	house.datasetx2 = df["Charms"]
	house.houses = df["Hogwarts House"]
	setminmax(house)
	setcount(house)
	iteration = 0
	print("Training Ravenclaw")
	diff = 1
	while (abs(diff) > 0.0001):
		print("Iteration " + str(iteration))
		oldcost = getcostfunction(house)
		train(house)
		diff = oldcost - getcostfunction(house)
		iteration = iteration + 1
	model.write(str(house.theta0) + "," + str(house.theta1) + "," + str(house.theta2) + "\n")
	house = House("Slytherin")
	house.datasetx1 = df["Divination"]
	house.datasetx2 = df["Defense Against the Dark Arts"]
	house.houses = df["Hogwarts House"]
	setminmax(house)
	setcount(house)
	iteration = 0
	print("Training Slytherin")
	diff = 1
	while (abs(diff) > 0.0001):
		print("Iteration " + str(iteration))
		oldcost = getcostfunction(house)
		train(house)
		diff = oldcost - getcostfunction(house)
		iteration = iteration + 1
	model.write(str(house.theta0) + "," + str(house.theta1) + "," + str(house.theta2) + "\n")


def main():
    if (len(sys.argv) == 1):
        print("logreg_train.py: missing dataset")
    else:
        dataset = open(str(sys.argv[1]), 'r')
        df = pandas.read_csv(dataset)
        prepare(df)

if __name__ == "__main__":
    # execute only if run as a script
    main()