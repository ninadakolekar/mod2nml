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



