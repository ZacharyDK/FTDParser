# FTDPharser
 Used to build csv files for any desired ticker from FTD data

 #
The purpose of this program is to assit in analyzing FTD for a specific ticker from the SEC
Data: https://www.sec.gov/data/foiadocsfailsdatahtm

It will read N number of FTD files, 
look for a specific ticker symbol, get that file line and remember it.
Once we read all the files in the data folder, we write all the lines we
remembered to one output file. 


Additionally, I substitute all '|' for ','. Helps with csv making.

Requires that you download python to use. 

The file "config.txt" is used to set the settings for the program. 
The first line is describes each setting.
The second line is the value of the setting.

Ticker = Stock Symbol you want to analyze 
InputFolder = Folder in the current working directory that you have the SEC FTD data
OutputFolder = Name of the Output Folder
OverrideOutputFolder = boolean. If true, we will delete any directory named OutputFolder and make a fresh one. If false, and any directory 
named OutputFolder already exists, I won't override any existing directories. Instead, I make one called OutputFolder2, or OutputFolder3, etc.