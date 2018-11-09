import sys
import os
import pprint 

import airspeed

# Custom modules
import util

pp = pprint.PrettyPrinter(depth=4)

def lexer(modFile):

    blocks = {}
    data = {}

    modFileData = [(str(line.strip())).replace('\t',' ') for line in open(modFile)]

    currentLineNumber = 0

    while(currentLineNumber<len(modFileData)):
        
        line = modFileData[currentLineNumber]

        if len(line)>0:

            # Title of the mod file
            if line.startswith('TITLE'):
                
                blocks['TITLE'] = line[6:].strip()
            
            if '{' in line:
                braceIndex = lines.index('{')
                blockHeading = lines[:braceIndex].strip()

                # Check if block heading is valid
                if util.isValidBlock(blockHeading):
                    
                    # Initialize empty list to store the parameters specified in this block
                    blocks[blockHeading] = []

                    dictData = lines[braceIndex+1:]
                    braceCount = checkBraces(dictData,1)

                    while braceCount>0:
                        
                        # If data in dataDict
                        if(len(dictData)>0):
                            blocks[blockHeading].append(dictData)
                        
                        currentLineNumber+=1

                        dictData = modFileData[currentLineNumber]

                        braceCount = checkBraces(dictData,braceCount)

                    newData = dictData[:-1].strip()
                    if len(newData)>0:
                        blocks[blockHeading].append(newData)

        currentLineNumber+=1
    
    stateBlock = blocks['STATE']

    for line in stateBlock:
        if ' ' in line or '\t' in line:
            stateBlock.remove(line)
            for state in line.split():
                blocks['STATE'].append(state)


                    



