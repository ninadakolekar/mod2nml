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

            if modFileData[currentLineNumber].startswith('?'):
                currentLineNumber+=1
                continue

            # Title of the mod file
            if line.startswith('TITLE'):
                
                blocks['TITLE'] = line[6:].strip()

            
            if '{' in line:
                braceIndex = line.index('{')
                blockHeading = line[:braceIndex].strip()

                # Check if block heading is valid
                if util.isValidBlock(blockHeading):

                    # Initialize empty list to store the parameters specified in this block
                    if blockHeading.startswith('PROCEDURE'):
                        blockHeading = 'PROCEDURE'
                    blocks[blockHeading] = []

                    dictData = [dataline for dataline in line[braceIndex+1:] if not dataline.startswith('?')]

                    braceCount = util.checkBraces(dictData,1)

                    # Loop until block terminates    
                    while braceCount>0:
                        if isinstance(dictData,str) and dictData.startswith('?'):
                            currentLineNumber+=1
                            dictData = modFileData[currentLineNumber]
                            continue 
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
                data['species'] = line.split("WRITE")[1].split()[0]

    gateList = []

    for state in stateBlock:
        gate = {}
        gate['id'] = state
        gate['instances'] = countInstances(breakpointBlock,state)
        gate['closed'] = state + str(0)
        gate['open'] = state
        gate['forwardEquationForm'] = getEquationForm()
        gate['backwardEquationForm'] = getEquationForm()
        gateList.append(gate)
        
    data['gates'] = gateList

    data['type'] = 'ionChannelHH'

    procedureBlock = blocks['PROCEDURE']

    if verbose:
        import pprint
        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(blocks)
    
    return data

# Ankur, please complete this function
def getEquationForm():
    return ''

def countInstances(br,ch):
    count = 0
    for s in br:
        sl = s.replace(" ","").split('*')   
        for x in sl:
            if ('^' in x) and x.split('^')[0].strip().replace("(","")==ch:
                count+=int(x.split('^')[1].replace(")",""))
            elif x==ch:
                count+=1
    return str(count)

# Input is list of statements of procedure block
def procParser(procedureBlock):
    line = ""
    procDict = {}
    procDict['SYMTAB'] = {}
    for item in procedureBlock:
        if item.replace(" ","").endswith(','):
            line+=item.replace(" ","")
        else:
            line+=item.replace(" ","")
            if line.startswith('LOCAL'):
                procDict['LOCAL'] = line[5:].strip().split(',')
                line = ""
            elif line.strip().startswith(tuple([x.replace(" ","") for x in procDict['LOCAL']])) and line.count('=')==1:
                exp = line.split('=')
                procDict['SYMTAB'][exp[0].replace(" ","")] = exp[1].replace(' ','')
                line=""
    return procDict
            

if __name__=="__main__":
    lexer("../examples/mod/KCa_Channel.mod",True)