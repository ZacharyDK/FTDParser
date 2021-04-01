
#Copyright Zachary Kolansky, 2021. 
#Use as you like

import os,shutil
from distutils.util import strtobool

'''
The purpose of this program is to assit in analyzing FTD for a specific ticker from the SEC
Data: https://www.sec.gov/data/foiadocsfailsdatahtm

It will read N number of FTD files, 
look for a specific ticker symbol, get that file line and remember it.
Once we read all the files in the data folder, we write all the lines we
remembered to one output file. 


Additionally, I substitute all '|' for ','. Helps with csv making

'''


'''
returns the ticker,inputFolder,and outputFolder
from a given configuration file
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

#MAIN
ticker,inputFolder,outputFolder,override = GetConfigurationSettings()
outputFolder = MakeNewDirectory(outputFolder,override)

if(os.path.isdir(inputFolder)):
    os.chdir(inputFolder) 
else:
    raise FileNotFoundError("InputFolder for data " + inputFolder + " not found! Can't continue!")

dataFileList = os.listdir() # get all the text files in the folder.

listOfRelevantTickerLines = []

fileHeader = ""
bDoOnce = True

for dataFileName in dataFileList:
    dataFile = open(dataFileName,'r')
    data = dataFile.readlines()
    for line in data:
        lineAsList = line.split('|')
        if(len(lineAsList) < 3):
            break #prevent index out of bounds error, likely from EOL
        if(lineAsList[2] != ticker):
            continue
        else:
            lineReplaced = line.replace('|',',') # want csv file
            listOfRelevantTickerLines.append(lineReplaced.strip())
    dataFile.close()
    if(bDoOnce): #get the header to write to the outfile, assume all input files are formatted the same
        dataFile = open(dataFileName,'r')
        fileHeaderRaw = dataFile.readline().strip()
        fileHeader = fileHeaderRaw.replace('|',',') # want csv file
        dataFile.close()
        bDoOnce = False

os.chdir('../')
os.chdir(outputFolder)
#print(os.getcwd())


outputFile = open("output.txt",'w')
outputFile.write(fileHeader + '\n')

for line in listOfRelevantTickerLines:
    outputFile.write(line + '\n')

os.chdir('../')
outputFile.close() #flush the text to write to the actual file
print("-------------------------\n")
print("Finished for Ticker " + ticker + " !" + '\n')
print("-------------------------\n")

if(ticker == "GME"):
    print("Power to the players.\n")

        


