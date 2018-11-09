import sys
import os

import airspeed

# Custom modules
import util

def lexer(modFile,verbose=False):
    
    try:
        open(modFile)
    except FileNotFoundError:
        print(f'File not found: {modFile}')
        exit()

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
                braceIndex = line.index('{')
                blockHeading = line[:braceIndex].strip()

                # Check if block heading is valid
                if util.isValidBlock(blockHeading):
                    
                    # Initialize empty list to store the parameters specified in this block
                    blocks[blockHeading] = []

                    dictData = line[braceIndex+1:]
                    braceCount = util.checkBraces(dictData,1)

                    while braceCount>0:
                        
                        # If data in dataDict
                        if(len(dictData)>0):
                            blocks[blockHeading].append(dictData)
                        
                        currentLineNumber+=1

                        dictData = modFileData[currentLineNumber]

                        braceCount = util.checkBraces(dictData,braceCount)

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

    neuronBlock = blocks['NEURON']
    breakpointBlock = blocks['BREAKPOINT']

    for line in neuronBlock:
        if line.startswith('SUFFIX'):
            data['id'] = line[7:].strip()
        if line.startswith('USEION'):
            if 'WRITE' in line:
                data['species'] = line.split()[1]

    gateList = []

    for state in stateBlock:
        gate = {}
        gate['id'] = state
        gate['instances'] = str(countInstances(breakpointBlock,state))
        gate['open'] = '<closed_state id="'+state+'0"/>'
        gate['open'] = '<closed_state id="'+state+'"/>'
        gateList.append(gate)
    
    data['gates'] = gateList

    data['type'] = 'ionChannelHH'

    if verbose:
        import pprint
        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(blocks)
    
    return data

def countInstances(br,ch):
  count = 0
  for s in br[1:]:
    sl = s.split('*')
    for x in sl:
      if ('^' in x) and x.split('^')[0]==ch:
        count+=int(x.split('^')[1])
      elif x==ch:
        count+=1
  return count


if __name__=="__main__":
    lexer("../examples/mod/neuron.mod",True)


