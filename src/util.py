def checkBraces(inputString, braceCounter):
    if len(inputString)>0:
        for c in inputString:
            if c=='{':
                braceCounter+=1
            elif c=='}':
                braceCounter-=1
    return braceCounter

def feedData(templateFile,data):
    with open(templateFile) as f:
        feeder = airspeed.Template(f.read())
    return feeder.merge(data)

def isValidBlock(string blockHeading):
    blocks = ['TITLE','UNITS','NEURON','PARAMETER','ASSIGNED','STATE','PROCEDURE','DERIVATIVE','BREAKPOINT','INITIAL','UNITSOFF','UNITSON']
    if blockHeading in blocks:
        return True
    else:
        return False