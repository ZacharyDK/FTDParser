import os,shutil
from distutils.util import strtobool

import StockDataReader as SDR



if __name__ == "__main__":
    ticker,inputFolder,outputFolder,override = SDR.GetConfigurationSettings("configShortVolume.txt")
    outputFolder = SDR.MakeNewDirectory(outputFolder,override)

    if(os.path.isdir(inputFolder)):
        os.chdir(inputFolder) 
    else:
        raise FileNotFoundError("InputFolder for data " + inputFolder + " not found! Can't continue!")

    
    MonthFolderList = os.listdir() # get all the folders in the data folder



    #Get all the Short volume data for each month
    fileHeader = ""
    TotalTickerLines = []
    for folder in MonthFolderList:
        if(os.path.isdir(folder)):
            os.chdir(folder) 
        else:
            continue

        fileList = os.listdir()

        

        fileHeader, tickerLines = SDR.ReadFilesForTicker(ticker,1,fileList)
        TotalTickerLines.extend(tickerLines)
       
        os.chdir('../')

    os.chdir('../') #back to root folder
    SDR.Output(outputFolder,fileHeader,TotalTickerLines)
    print('\n' + "Finished for ticker " + ticker + '\n')
 