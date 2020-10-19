import cv2
import numpy as np
import os
from os.path import isfile, join
import time
import sys
import imageio

path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

imageFolder = os.path.join(path, "Captures", "Captures_Today")

logstdout = os.path.join(path, "Logs", "stdout-video_creator_pyw.txt")
logstderr = os.path.join(path, "Logs", "stderr-video_creator_pyw.txt")
#if sys.executable.endswith("python.exe"):
sys.stdout = open(logstdout, "w")
sys.stderr = open(logstderr, "w")

folderFinalName = time.strftime("%Y_%m_%d_Captures")

CONFIG_GIF_DURATION_FROM_COUNT = False
CONFG_GIF_FRAMES_PER_SECOND = 24
CONFIG_GIF_DURATION_SECONDS = 5

def GetListOfFilesRecursive(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            #print("Dir: "+fullPath)
            allFiles = allFiles + GetListOfFilesRecursive(fullPath)
        else:
            if fullPath.endswith( ('.jpeg', '.png', '.jpg') ):
                allFiles.append(fullPath)
                #print("File: "+fullPath)
                
    return allFiles  

def CreateVideoFromFolder(folder):

    if not os.path.exists(folder):
        print("Folder "+folder+"not found")
        return
    filenames = []
    count = 0.0

    for file in os.listdir(folder):
        count += 1.0
        filename = os.path.join(folder, file)
        #print(filename)
        if filename.endswith( ('.jpeg', '.png', '.jpg') ):
            filenames.append(filename)

    filenames.sort() # this iteration technique has no built in order, so sort the frames

    fps = 1.0

    if CONFIG_GIF_DURATION_FROM_COUNT:
        fps = count/CONFIG_GIF_DURATION_SECONDS
    else:
        fps = CONFG_GIF_FRAMES_PER_SECOND

    frame_array = []
    for image in filenames:
        img = cv2.imread(image)
        height, width, layers = img.shape
        size = (width,height)
        frame_array.append(img)
    out = cv2.VideoWriter(os.path.join(folder, 'movie.mp4'),cv2.VideoWriter_fourcc(*'avc1'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

def verify_image(img_file):
    try:
        img = cv2.imread(img_file)
    except:
        return False
    return True

def CreateVideoFromList(filenames):

    fps = 1.0

    if CONFIG_GIF_DURATION_FROM_COUNT:
        fps = count/CONFIG_GIF_DURATION_SECONDS
    else:
        fps = CONFG_GIF_FRAMES_PER_SECOND

    img = cv2.imread(filenames[0])

    height, width, layers = img.shape
    size = (width,height)

    out = cv2.VideoWriter(os.path.join(path, 'Captures', 'movie.mp4'),cv2.VideoWriter_fourcc(*'avc1'), fps, size)
    frame_array = []
    for image in filenames:
        if verify_image(image):
            out.write(cv2.imread(image))
        else:
            print("ERROR: \n")
            print(image)
    out.release()


# CreateVideoFromFolder(imageFolder)

listOfFiles = list()
listOfFiles = GetListOfFilesRecursive(os.path.join(path, "Captures"))
listOfFiles.sort()

CreateVideoFromList(listOfFiles)

if os.path.exists(imageFolder):
    os.rename(imageFolder, os.path.join(path, "Captures", folderFinalName))