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
    meanx1 = float('NaN')
    meanx2 = float('NaN')
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
    	if (math.isnan(x1)):
    		x1 = self.meanx1
    	if (math.isnan(x2)):
    		x2 = self.meanx2
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

def setmean(house):
	total = 0
	count = 0
	for value in house.datasetx1:
		count = count + 1
		if not math.isnan(value):
			total += value
	house.meanx1 = total / count
	total = 0
	count = 0
	for value in house.datasetx2:
		count = count + 1
		if not math.isnan(value):
			total += value
	house.meanx2 = total / count


def setcount(house):
	count = 0
	for value in house.houses:
		count = count + 1
	house.count = count


def predict(df, model):
	csv = open("houses.csv", 'w')
	csv.write("Index,Hogwarts House\n")
	count = 0
	for value in df["Index"]:
		count = count + 1
	index = 0
	houseGryffindor = House("Gryffindor")
	houseGryffindor.datasetx1 = df["Flying"]
	houseGryffindor.datasetx2 = df["Transfiguration"]
	houseGryffindor.houses = df["Hogwarts House"]
	setminmax(houseGryffindor)
	setcount(houseGryffindor)
	setmean(houseGryffindor)
	line = model.readline()
	split = line.split(',')
	if (not split[0] or not split[1] or not split[2]):
		print("File badly formated")
		return
	houseGryffindor.theta0 = float(split[0])
	houseGryffindor.theta1 = float(split[1])
	houseGryffindor.theta2 = float(split[2])
	print("Gryffindor:")
	print("theta0:", str(houseGryffindor.theta0))
	print("theta1:", str(houseGryffindor.theta1))
	print("theta2:", str(houseGryffindor.theta2))
	houseRavenclaw = House("Ravenclaw")
	houseRavenclaw.datasetx1 = df["Charms"]
	houseRavenclaw.datasetx2 = df["Muggle Studies"]
	houseRavenclaw.houses = df["Hogwarts House"]
	setminmax(houseRavenclaw)
	setcount(houseRavenclaw)
	setmean(houseRavenclaw)
	line = model.readline()
	split = line.split(',')
	if (not split[0] or not split[1] or not split[2]):
		print("File badly formated")
		return
	houseRavenclaw.theta0 = float(split[0])
	houseRavenclaw.theta1 = float(split[1])
	houseRavenclaw.theta2 = float(split[2])
	print("Ravenclaw:")
	print("theta0:", str(houseRavenclaw.theta0))
	print("theta1:", str(houseRavenclaw.theta1))
	print("theta2:", str(houseRavenclaw.theta2))
	houseSlytherin = House("Slytherin")
	houseSlytherin.datasetx1 = df["Divination"]
	houseSlytherin.datasetx2 = df["Defense Against the Dark Arts"]
	houseSlytherin.houses = df["Hogwarts House"]
	setminmax(houseSlytherin)
	setcount(houseSlytherin)
	setmean(houseSlytherin)
	line = model.readline()
	split = line.split(',')
	if (not split[0] or not split[1] or not split[2]):
		print("File badly formated")
		return
	houseSlytherin.theta0 = float(split[0])
	houseSlytherin.theta1 = float(split[1])
	houseSlytherin.theta2 = float(split[2])
	print("Slytherin:")
	print("theta0:", str(houseSlytherin.theta0))
	print("theta1:", str(houseSlytherin.theta1))
	print("theta2:", str(houseSlytherin.theta2))
	error = 0
	while (index < count):
		# print(df["Hogwarts House"][index])
		if (houseGryffindor.getx(houseGryffindor.datasetx1[index], houseGryffindor.datasetx2[index]) < 0):
			house = "Gryffindor"
		elif (houseRavenclaw.getx(houseRavenclaw.datasetx1[index], houseRavenclaw.datasetx2[index]) < 0):
			house = "Ravenclaw"
		elif (houseSlytherin.getx(houseSlytherin.datasetx1[index], houseSlytherin.datasetx2[index]) < 0):
			house = "Slytherin"
		else:
			house = "Hufflepuff"
		if (df["Hogwarts House"][index] and house != df["Hogwarts House"][index]):
			print(df["Hogwarts House"][index])
			hx = houseGryffindor.getx(houseGryffindor.datasetx1[index], houseGryffindor.datasetx2[index])
			print(hx)
			hx = houseRavenclaw.getx(houseRavenclaw.datasetx1[index], houseRavenclaw.datasetx2[index])
			print(hx)
			hx = houseSlytherin.getx(houseSlytherin.datasetx1[index], houseSlytherin.datasetx2[index])
			print(hx)
			error = error + 1
			print(house)
		elif (df["Hogwarts House"][index]):
			hx1 = houseGryffindor.getx(houseGryffindor.datasetx1[index], houseGryffindor.datasetx2[index])
			hx2 = houseRavenclaw.getx(houseRavenclaw.datasetx1[index], houseRavenclaw.datasetx2[index])
			hx3 = houseSlytherin.getx(houseSlytherin.datasetx1[index], houseSlytherin.datasetx2[index])
			if (math.isnan(hx1) or math.isnan(hx2) or math.isnan(hx3)):
				print(index)
				print("hx1:", hx1)
				print("hx2:", hx2)
				print("hx3:", hx3)
				print(house)
				error = error + 1
		# print(house)
		csv.write(str(index) + "," + house + "\n")
		index = index + 1
	print("Error", error)


def main():
    if (len(sys.argv) == 1):
        print("logreg_predict.py: missing dataset")
    elif (len(sys.argv) == 2):
        print("logreg_predict: missing model")
    else:
        dataset = open(str(sys.argv[1]), 'r')
        model = open(str(sys.argv[2]), 'r')
        df = pandas.read_csv(dataset)
        predict(df, model)

if __name__ == "__main__":
    # execute only if run as a script
    main()