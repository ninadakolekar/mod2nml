import airspeed

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

def isValidBlock(blockHeading):
    # Check for procedure block
    if(blockHeading.startswith('PROCEDURE')):
        return True
    else:
        blocks = ['TITLE','UNITS','NEURON','PARAMETER','ASSIGNED','STATE','PROCEDURE','DERIVATIVE','BREAKPOINT','INITIAL','UNITSOFF','UNITSON']
        if blockHeading in blocks:
            return True
        else:
            return False

def func(opIndexList,newVars,expr):
    res = ""
    k = 0
    i= 0
    while i in range(len(expr)):
        if str(i) in opIndexList:
            res+=expr[i]
            i+=1
        else:
            res+=newVars[k]
            i+=len(newVars[k])
            k+=1
    print(res)

def raiseLexicalError(err):
    import sys
    print(f"Error: {err}", file=sys.stderr)
    exit(1)

def raiseSyntaxError(err):
    import sys
    print(f"Syntax Error: {err}", file=sys.stderr)
    exit(1)

if __name__=='__main__':
    func(['1', '5', '6', '8', '10', '11', '13'],['3', 'exp', 'x', '3', '4'],"3*exp((x-3)/4)")