import os
import sys
import datetime

import numpy as np


#Define fixed indices for columns of interest
i_recID = 0
i_name = 7
i_zipCode = 10
i_tDate = 13
i_tAmount = 14
i_other = 15
#Define number of columns in each row
numCols = 21

def main(argv):

#    percFileName = 'insight_testsuite/tests/test_1/input/percentile.txt'
    percFileName = 'input/percentile.txt'
    perc = -1
    with open(percFileName) as percFile:
        perc = float(percFile.readline().strip())


    if(perc <=0 or perc > 100):
        raise ValueError('Percent input invalid! Must be > 0 and <= 100\n')
        
    print('Calculate percentile at ' + str(perc) + ' percent\n')
    
    #Control inputs
    
    donors = {}
    records = {}

    #TEMPORARY
    #    inFileName = 'insight_testsuite/tests/test_1/input/itcont.txt'
    inFileName = 'input/itcont.txt'
    #    outFileName = 'insight_testsuite/tests/test_1/output/repeat_donors.txt'
    outFileName = 'output/repeat_donors.txt'

    #I/O??? STREAMING?
    with open(inFileName,'r') as inFile, open(outFileName,'w') as outFile:

        recordCount = 0

        for line in inFile:
            recordCount+=1

            inList = line.strip().split('|')
            
            if (len(inList) != numCols):
                sys.stderr.write('This line has ' + str(len(inList)) + ' columns, not ' + str(numCols)+'\n')
                continue
            
            #The condition below does not correspond to an error in the data, so we silently skip it.
            if (inList[i_other]):
                continue

            recID = inList[i_recID]
            donorName = inList[i_name]
            zipCode = inList[i_zipCode][0:5]
            tDate = datetime.datetime.strptime(inList[i_tDate],'%m%d%Y')
            tAmount = int(round(float(inList[i_tAmount])))
            
            donorKey = donorName + zipCode
            #print(donorKey)

            if donorKey not in donors:
                firstTyr = tDate.year
                donors[donorKey] = [0,firstTyr]
            elif tDate.year <= donors[donorKey][1]:
                #Encountered a transaction from this donor that came before the "first" one: skip this.
                continue
            else:
                recordKey = recID + str(tDate.year) + zipCode
                #print(recordKey)

                if recordKey not in records:
                    records[recordKey] = []

                records[recordKey].append(tAmount)
                percVal = np.percentile(records[recordKey],perc,interpolation='nearest')
                
                tNum = len(records[recordKey])
                tSum = sum(records[recordKey])
            
                outputStr= (recID + '|' + zipCode + '|' + str(tDate.year) + '|' + str(percVal) +
                          '|' + str(tSum) + '|' + str(tNum)) + '\n'

                print(outputStr.strip())
                outFile.write(outputStr)
    
        
if __name__ == "__main__":
    main(sys.argv)
