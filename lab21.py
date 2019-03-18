from time import sleep
from drive import RosAriaDriver
import math
import json

robot=RosAriaDriver('/PIONIER6')

import matplotlib.pyplot as plt
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import time


from lab5 import world_map

scan = []
theta = []
data = list()

outputPath = "./output/"
inputPath = "./datafiles/"


def readJSON(filename):
    json_file = open(filename)
    data = json.load(json_file)
    return data

def saveJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def convertDataToGlobalCoordinates(data):
    x = np.arange(0, 512)
    theta = (np.pi / 512) * x

    pointsHit = list()

    for iteration in data:
        pointsHitTemp = list()

        iteration['pose'][2] = np.deg2rad(iteration['pose'][2])

        for scanIndex in range(len(iteration['scan'])):

            if not np.isinf(iteration['scan'][scanIndex]) and not np.isnan(iteration['scan'][scanIndex]):
                scanPointX = iteration['pose'][0] + 0.18 * math.cos(iteration['pose'][2]) + iteration['scan'][
                    scanIndex] * math.cos(iteration['pose'][2] + theta[scanIndex])
                scanPointY = iteration['pose'][1] + 0.18 * math.sin(iteration['pose'][2]) + iteration['scan'][
                    scanIndex] * math.sin(iteration['pose'][2] + theta[scanIndex])
                pointsHitTemp.append([scanPointX, scanPointY])

        pointsHit.append(pointsHitTemp)
    return pointsHit


def robotScanData():
    data = []
    for i in range(10):
        dataPoint = []
        dataPoint['pose'] = robot.GetPose()
        dataPoint['scan'] = robot.ReadLaser()
        robotScanData(outputPath + "pointsHit.JSON", pointsHit)
        data.append(dataPoint)
        time.sleep(5)

    saveJSON(outputPath + "pointsHit.JSON", data)


if __name__ == '__main__':
    wm=world_map(16,16,0.1)
    wm.initialize_map()

    # data = readJSON(inputPath + "map_round.json")

    robotScanData()
    exit(0)
    # poses = [item['pose'] for item in data]



    pointsHit = convertDataToGlobalCoordinates(data)



    saveJSON(outputPath + "pointsHit.JSON", pointsHit)

    # for iter in pointsHit:
    #     wm.updateHitCells(iter)


    # for iter in pointsHit:
    #     wm.updateHitCells(iter)


    wm.updateHitCells(pointsHit[0])
    wm.updateHitCells(pointsHit[1])

    wm.updateProbabilityMap()
    mapa = np.asarray(wm.probabilityMap, dtype=np.float32)

    # TODO Skalowanie mapy z indeksow na wlasciwe koordynaty
    # TODO Przejrzec przetwarzanie danych, bo cos nie pasuje z wartosciami. Sa jakby ucinane

    # saveJSON(outputPath + "temp.JSON", wm.mapa)
    # W drugije iteracji powinien sie wykres tylko przesunac w prawo/lewo o 0.5m


    plt.imshow(mapa, interpolation="nearest", cmap='Blues')
    plt.grid(True, 'both')
    # plt.axes().plot([pos[0] for pos in poses], [pos[1] for pos in poses])
    plt.colorbar()
    plt.show()
