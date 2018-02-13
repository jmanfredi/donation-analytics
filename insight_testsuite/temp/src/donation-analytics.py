#!/usr/bin/env python3
import os
import sys
import datetime
from contextlib import contextmanager

import numpy as np

from dautilities import smart_open,calc_percentile

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
    
    percFileName = argv[1]
    inFileName = argv[2]
    outFileName = argv[3]
    
    perc = -1
    with smart_open(percFileName) as (percFile,err):
        if err:
            raise IOError('Unable to open percent input file: '+percFileName+'\n')
        else:
            perc = float(percFile.readline().strip())


    if(perc <=0 or perc > 100):
        raise ValueError('Percent input invalid! Must be > 0 and <= 100\n')
        
    donors = {}
    repeats = {}
    
    with smart_open(inFileName,'r') as (inFile,inErr), smart_open(outFileName,'w') as (outFile,outErr):
        if inErr:
            raise IOError('Unable to open input file: '+inFileName+'\n')
        elif outErr:
            raise IOError('Unable to open output file: '+outFileName+'\n')
        else:
            recordCount = 0
            
            for line in inFile:
                recordCount+=1
                
                inList = line.strip().split('|')
                
                if (len(inList) != numCols):
                    sys.stderr.write('Line '+str(recordCount)+' has ' + str(len(inList)) + ' columns, not ' + str(numCols)+'. Skipping.\n')
                    continue
            
                #The condition below does not correspond to an error in the data, so we silently skip this line.
                if (inList[i_other]):
                    continue

                recID = inList[i_recID]
                if (recID==''):
                    sys.stderr.write('Line '+str(recordCount)+' has an empty recipientID. Skipping.\n')
            
                donorName = inList[i_name]
                if (donorName==''):
                    sys.stderr.write('Line '+str(recordCount)+' has an empty name. Skipping.\n')
                
                zipCode = inList[i_zipCode][0:5]
                if (len(zipCode) < 5):
                    sys.stderr.write('Line '+str(recordCount)+' has a bad zipcode: '+zipCode+'. Skipping.\n')
                    continue
            
                try:
                    tDate = datetime.datetime.strptime(inList[i_tDate],'%m%d%Y')
                except ValueError:
                    sys.stderr.write('Line ' +str(recordCount)+' has bad datetime. Skipping.\n')
                    continue

                try:
                    tAmount = int(round(float(inList[i_tAmount])))
                except ValueError:
                    sys.stderr.write('Line '+str(recordCount)+' has a bad transaction amount. Skipping.\n')
            

                donorKey = donorName + zipCode

                if donorKey not in donors:
                    firstTyr = tDate.year
                    donors[donorKey] = firstTyr
                elif tDate.year < donors[donorKey]:
                    #Encountered a transaction from this donor that came before the "first" one: skip this.
                    continue
                else:
                    repeatKey = recID + str(tDate.year) + zipCode
                    if repeatKey not in repeats:
                        repeats[repeatKey] = []

                    repeats[repeatKey].append(tAmount)
                    percVal = calc_percentile(repeats[repeatKey],perc)

                    tNum = len(repeats[repeatKey])
                    tSum = sum(repeats[repeatKey])
            
                    outputStr= (recID + '|' + zipCode + '|' + str(tDate.year) + '|' + str(percVal) +
                                '|' + str(tSum) + '|' + str(tNum)) + '\n'

                    outFile.write(outputStr)


    
if __name__ == "__main__":
    main(sys.argv)
