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

def equationParser(expr):
    flag = 0
    string1 = re.compile('[(]*\d+[)]*[*][e][x][p][(]*[A-Za-z]+[-]\d+[)]*[/][(]*\d+[)]*')
    
    if (len(string1.findall(expr)) != 0 and string1.findall(expr)[0] == True):
        print('exponential')
        flag = 1
    else:
        string1 = re.compile('[(]*\d+[)]*\s[/]\s[(]*[e][x][p][(]*\w+\s[-]\d+[)]*[/]\s\d+[)]*')
    if(string1.search(expr) is not None):
        print('sigmoid')
        flag = 2
    else:
        string1 = re.compile('[(]*\d+[)]*[*][(]*\w+\s[-]\s\d+[)]*[/][(]*\d+[)]*[/][(]*[1]\s[-]\s[e][x][p][(]*\w+\s[-]\s\d+[)]*[/][(]*\d+[)]*')
        if (string1.search(expr)!=None):
            flag = 3
        else:
            print('generic')
            flag = 4


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