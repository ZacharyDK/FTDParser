#Copyright Zachary Kolansky, 2021. 
#Use as you like

import os,shutil
from distutils.util import strtobool


'''
returns the ticker,inputFolder, outputFolder, and override
from a given configuration file

override: Whether to override the output folder.
'''
def GetConfigurationSettings(configFileName = "config.txt"):
    config = open(configFileName,'r')

    configAsList = config.readlines() #convert config file to a list
    configString = configAsList[1] #has config data in the second line, 0 = first line
    configSplit = configString.split(',')


    ticker = configSplit[0].strip() #removal \n, other whitespace
    inputFolder = configSplit[1].strip()
    outputFolder = configSplit[2].strip()
    override = strtobool(configSplit[3].strip().lower())
    config.close()
    return ticker,inputFolder,outputFolder,override


'''
If override is true, we delete the contents of a given directory, then make a new directory of the same name
if override is false, we will make a new directory, with name equal Directory + N, where N is number of directories in the current working directory
that have the given Directory name. This means if there is already a folder called Output, we will make a folder called Output2 and so on

returns the name of directory this function creates. 
'''
def MakeNewDirectory(Directory,override = True):
    FinalDirectoryName = Directory
    if(override):
        if(os.path.exists(Directory)):
            shutil.rmtree(Directory)
            os.mkdir(Directory)
        else:
            os.mkdir(Directory)


    else: #make new seperate folder
        if(os.path.exists(Directory)):
            cwdFiles = os.listdir()
            numberOfSimiliarlyNamedDir = int(str(cwdFiles).count(Directory) + 1) #number of output folders
            NewDirName = Directory + str(numberOfSimiliarlyNamedDir) #create valid output file folder
            os.mkdir(NewDirName)
            FinalDirectoryName = NewDirName
        else:
            os.mkdir(Directory)

    return FinalDirectoryName


'''
Input:  Ticker, TickerIndex, encoding of files  dataFileList,
Data files to read {Array of string file name}, 
encoding = 'latin'
TickerIndex: After spliting a dataline by |, what index would contain the given ticker info

Output FileHeader {String}, TickerLines {Array of Strings}

 
'''
def ReadFilesForTicker(ticker,tickerIndex = 2,dataFileList = []):
    listOfRelevantTickerLines = []

    fileHeader = ""
    bDoOnce = True

    for dataFileName in dataFileList:
        dataFile = open(dataFileName,'r',encoding='latin1')
        #dataFile = open(dataFileName,'r',encoding)
        data = dataFile.readlines()
        for line in data:
            lineAsList = line.split('|')
            if(len(lineAsList) < 3):
                break #prevent index out of bounds error, likely from EOL
            if(lineAsList[tickerIndex] != ticker):
                continue
            else:
                lineReplaced = line.replace('|',',') # want csv file
                #listOfRelevantTickerLines.append(dataFileName + ',' + lineReplaced.strip())
                listOfRelevantTickerLines.append(lineReplaced.strip())
        dataFile.close()
        if(bDoOnce): #get the header to write to the outfile, assume all input files are formatted the same
            dataFile = open(dataFileName,'r')
            fileHeaderRaw = dataFile.readline().strip()
            fileHeader = fileHeaderRaw.replace('|',',') # want csv file
            dataFile.close()
            bDoOnce = False

    return fileHeader,listOfRelevantTickerLines

'''
Writes given data to an output file

outputFolder name of folder we want to write to
fileHeader header describing the data in the array
tickerLines = Array of strings to write
outputFileName = of the output file
'''
def Output(outputFolder,fileHeader, tickerLines,outputFileName = "output.txt"):
    if(os.path.isdir(outputFolder)):
        os.chdir(outputFolder) 
    else:
        os.chdir('../') #try again...if this fails, then we raise an error

        if(os.path.isdir(outputFolder)):
            os.chdir(outputFolder)
        else: 
            raise FileNotFoundError("outputFolder for data " + outputFolder + " not found! Can't continue!")

    outputFile = open(outputFileName,'w')
    outputFile.write(fileHeader + '\n')

    for line in tickerLines:
        outputFile.write(line + '\n')

    os.chdir('../')
    outputFile.close() #flush the text to write to the actual file
  
    

    