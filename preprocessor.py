import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from PIL import Image

def PreProcess(inputImage):
    path = 'D:/Class 12 CS/CS Project/Images'######PREPROCESSED & SPLIT IMAGES ARE SAVED TO THIS DIR -> CHANGE PATH WHEN RUNNING LOCALLY
    inputImage = cv2.bitwise_not(inputImage)
    inputCopy = inputImage.copy()
    greyscaleImage = cv2.cvtColor(inputImage,cv2.COLOR_BGR2GRAY)

    windowSize = 31
    windowConstant = -1
    binaryImage = cv2.adaptiveThreshold(greyscaleImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,windowSize,windowConstant)

    minArea = 20
    componentsNumber, labeledImage, componentStats, componentCentroids = \
    cv2.connectedComponentsWithStats(binaryImage, connectivity=4)
    remainingComponentLabels = [i for i in range(1,componentsNumber) if componentStats[i][4]>= minArea]
    filteredImage = np.where(np.isin(labeledImage,remainingComponentLabels) == True,255,0).astype('uint8')

    kernelSize = 3
    opIterations = 1
    maxKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
    closingImage = cv2.morphologyEx(filteredImage, cv2.MORPH_CLOSE, maxKernel, None, None, opIterations, cv2.BORDER_REFLECT101)

    contours, hierarchy = cv2.findContours(closingImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours_poly = [None] * len(contours)
    boundRect = []
    for i, c in enumerate(contours):
        if hierarchy[0][i][3] == -1:
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect.append(cv2.boundingRect(contours_poly[i]))

    for i in range(len(boundRect)):
        color = (0, 255, 0)
        cv2.rectangle(inputCopy, (int(boundRect[i][0]), int(boundRect[i][1])), \
                  (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
    num=0
    for i in range(len(boundRect)):
        x, y, w, h = boundRect[i]
        croppedImg = closingImage[y:y + h, x:x + w]
        if croppedImg.size > 1000:
            #cv2.imwrite(f'{i}.png',croppedImg)
            cv2.imwrite(os.path.join(path , f'{num}.png'), croppedImg)
            num+=1

    i=0
    while True:
      try:
        img=Image.open(f'D:/Class 12 CS/CS Project/Images/{i}.png')
        img=img.resize((28,28))
        img.save(f'D:/Class 12 CS/CS Project/Images1/{i}.png')
        i+=1
      except:
        break

    return "Finished Preprocessing..."
