import sys
import os
import re
import airspeed
from math import *

import util

def lexer(modFile,verbose,config):
    
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
                    elif blockHeading.startswith('DERIVATIVE'):
                        blockHeading = 'DERIVATIVE'
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
    
    checkBlocks(blocks)

    procedureBlock = blocks['PROCEDURE']
    stateBlock = blocks['STATE']

    for line in stateBlock:
        if ' ' in line or '\t' in line:
            stateBlock.remove(line)
            for state in line.split():
                blocks['STATE'].append(state)

    neuronBlock = blocks['NEURON']
    breakpointBlock = blocks['BREAKPOINT']
    
    potential = potentials(neuronBlock, blocks['PARAMETER'],blocks['INITIAL'])
    for key in potential:
        data[key] = potential[key]

    for line in neuronBlock:
        if line.startswith('SUFFIX'):
            data['id'] = line[7:].strip()
        if line.startswith('USEION'):
            if 'WRITE' in line:
                data['species'] = line.split("WRITE")[1].split()[0]

    gateList = []
    procDict = procParser(procedureBlock,stateBlock)
    for state in stateBlock:
        gate = {}
        gate['id'] = state
        gate['instances'] = countInstances(breakpointBlock,state)
        gate['closed'] = state + str(0)
        gate['open'] = state
        gate['forwardEquationForm'] = getEquationForm()
        gate['backwardEquationForm'] = getEquationForm()
        gate['forwardEquationForm']  = 'generic'
        gate['backwardEquationForm']  = 'generic'
        gateProcDict = {}
        gateProcDict['LOCAL'] = procDict['LOCAL']
        gateProcDict['SYMTAB'] = {}
        print("k ",procDict['SYMTAB'][state]['alpha'])
        for key in procDict['SYMTAB']:
            if key not in stateBlock:
                gateProcDict['SYMTAB'][key] = procDict['SYMTAB'][key]
                gateProcDict['SYMTAB'][key] = procDict['SYMTAB'][key]
        gateProcDict['SYMTAB']['alpha'] = procDict['SYMTAB'][state]['alpha']
        gateProcDict['SYMTAB']['beta'] = procDict['SYMTAB'][state]['beta']
        if config['generic']:
            gate['forwardExpr'] = procDict['SYMTAB']['alpha']
            gate['backwardExpr'] = procDict['SYMTAB']['beta']
        else:
            
        gateList.append(gate)
        
    data['gates'] = gateList

    data['type'] = 'ionChannelHH'

    if verbose:
        import pprint
        pp = pprint.PrettyPrinter(depth=4)
        print("\n\n*** PARSING & IR ***\n\n")
        pp.pprint(procDict)
        print('\n\n**** LEXICAL ANALYSIS ****\n\n')
        pp.pprint(blocks)
    
    return data

def checkBlocks(blocksDict):
    blocks = ['TITLE','UNITS','NEURON','PARAMETER','ASSIGNED','STATE','PROCEDURE','BREAKPOINT','INITIAL']
    for block in blocks:
        if block not in blocksDict:
            util.raiseLexicalError(f"{block} block not found.")

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

def potentials(neuronBlock, paramBlock,initBlock):
    vDict = {}
    ion_read = ""
    for item in neuronBlock:
        line = item.split('?')[0]
        if line.startswith('USEION'):
            keywords = line.split(" ")
            vDict['ion'] = keywords[keywords.index('USEION')+1]
            if 'READ' == keywords[keywords.index('USEION')+2]:
                ion_read = keywords[keywords.index('USEION')+3]
            else:
                ion_read = 'e'+vDict['ion']
    if('ion' in vDict):
        for item in initBlock:
            line = item.split('?')[0]
            if line.startswith(ion_read) and '=' in line:
                vDict['initConc'] = str(evaluate(line.split('=')[1]))
    for item in paramBlock:
        line = item.split('?')[0]
        if line.startswith('gmax') and '=' in line:
            vDict['gmax'] = str(int(1000*evaluate(line.split('=')[1].split('(')[0])))
    return vDict

def procParser(procedureBlock,stateBlock):
    localFlag = False
    line = ""
    procDict = {}
    procDict['SYMTAB']={}
    for state in stateBlock:
        procDict['SYMTAB'][state] = {}
    count = 0
    for item in procedureBlock:
        if item.replace(" ","").endswith(','):
            line+=item.replace(" ","")
        else:
            line+=item.replace(" ","")
            if line.startswith('LOCAL'):
                localFlag = True
                procDict['LOCAL'] = line[5:].strip().split(',')
                line = ""
            elif 'LOCAL' not in procDict:
                util.raiseLexicalError("No LOCAL block found in PROCEDURE")
                exit(1)
            elif line.strip().startswith(tuple([x.replace(" ","") for x in procDict['LOCAL']])) and line.count('=')==1:
                numbers=re.compile('^([-+/*]\d+(\.\d+)?)*')
                exp = line.split('=')
                if(len(numbers.findall(exp[1]))==1 and exp[0].replace(" ","")!='alpha' and exp[0].replace(" ","")!='beta'):
                    procDict['SYMTAB'][exp[0].replace(" ","")] = str(evaluate(exp[1].split('?')[0].replace(' ','')))
                else:
                    procDict['SYMTAB'][stateBlock[count]][exp[0].replace(" ","")] = exp[1].split('?')[0].replace(' ','')
                    if line.startswith('beta') and count<len(state):
                        count+=1
                line=""
            else:
                if line.startswith('beta') and count<len(state):
                    count+=1
                line=""
    return procDict
  
def evaluate(expression):
    x = -1
    try:
        x = eval(expression)
    except SyntaxError as err:
        util.raiseSyntaxError('Unexpected EOF or invalid mathematical expression.')
        pass
    except NameError:
        return expression
    print("eval ",expression,"{:.10f}".format(float(x)))
    return x

if __name__=="__main__":
    lexer("../examples/mod/KCa_Channel.mod",True)