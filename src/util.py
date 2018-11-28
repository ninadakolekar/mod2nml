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

def combineboth(operatorindex,newvars,expr,b):

    res=""
    k=0
    i=0
    while i in range(len(expr)):
        if str(i) in operatorindex:
            res=res+expr[i]
            i+=1
        else:
            if newvars[k] in b :
                res=res+ b[newvars[k]]
            else:
                res=res+newvars[k]
            i+=len(newvars[k])
            k+=1
    
    return res

def substitutionwrapper(a):
    b={}
    c={}
    answer={}
    for item in a['LOCAL']:
        string3=re.compile('[-]?\d+')
        if(item in a['SYMTAB']):
            string1=a['SYMTAB'][item]
            if(len(string3.findall(string1))==1 and string3.findall(string1)[0] == string1):
                a['SYMTAB'][item]+='.'+'0'
            string1=a['SYMTAB'][item]
            string2=re.compile('[-]?\d+[.]\d+|[-]?\d+')
            if(len(string2.findall(string1))==1 and string2.findall(string1)[0] == string1):
                b[item]=string1
            else:
                c[item]=string1
    result=substituteconstant(a,b,c)
    i=0
    for item in a['LOCAL']:
        if(item in a['SYMTAB']): 
            string1=a['SYMTAB'][item]
            string2=re.compile('[-]?\d+[.]\d+|[-]?\d+')
            if(len(string2.findall(string1))==1 and string2.findall(string1)[0] == string1):
                b[item]=string1
            else:
                answer[item]=result[i]
                i+=1
    
    return answer

def substitutionwrappernon(a):
    b={}
    c={}
    answer={}
    for item in a['LOCAL']:
        string3=re.compile('[-]?\d+')
        if(item in a['SYMTAB']):
            string1=a['SYMTAB'][item]
            if(len(string3.findall(string1))==1 and string3.findall(string1)[0] == string1):
                a['SYMTAB'][item]+='.'+'0'
            string1=a['SYMTAB'][item]
            string2=re.compile('[-]?\d+[.]\d+|[-]?\d+')
            if(len(string2.findall(string1))==1 and string2.findall(string1)[0] == string1):
                b[item]=string1
            else:
                c[item]=string1
    result=substituteconstant(a,b,c)
    i=0
    for item in a['LOCAL']:
        if(item in a['SYMTAB']):
            string1=a['SYMTAB'][item]
            string2=re.compile('[-]?\d+[.]\d+|[-]?\d+')
            if(len(string2.findall(string1))==1 and string2.findall(string1)[0] == string1):
                b[item]=string1
            else:
                answer[item]=equationParser(result[i])
                i+=1
    return answer


def equationParser(expr):
    flag = 0
    string1 = re.compile('[(]*[-]?[\d+][.][\d+][)]*[*][e][x][p][(]*[A-Za-z]+[+-][-]?[\d+][.][\d+][)]*[/][-]?[\d+][.][\d+][)]*')
    if(len(string1.findall(expr))!=0 and string1.findall(expr)[0] == expr):
        flag = 1
    else:
        string1=re.compile('[(]*[-]?\d+[.][\d+][)]*[/][(]*[e][x][p][(]*[A-Za-z]+[+-][-]?\d+[.]\d+[)]*[/][(]*[-]?\d+[.]\d+[)]*[+][1][)]*')
        if(len(string1.findall(expr))!= 0 and string1.findall(expr)[0] == expr):
            flag = 2
        else:
            string1=re.compile('[(]*[-]?\d+[.]\d+[)]*[*][(]*[A-Za-z]+[-][-]?\d+[.]\d+[)]*[/][(]*[-]?\d+[.]\d+[)]*[/][(]*[1][-][e][x][p][(]*[-][(]*[A-Za-z]+[-][-]?\d+[.]\d+[)]*[/][(]*[-]?\d+[.]\d+[)]*')
            if(len(string1.findall(expr))!= 0 and string1.findall(expr)[0] == expr):
                flag = 3
            else:
                flag = 4
    a = {}
    if(flag == 1):
        string3=re.compile('[A-Za-z]+[-](\d+[.]\d+)')
        y=string3.findall(expr)
        string2=re.compile('[-]?\d+[.]\d+')
        x=string2.findall(expr)
        a['type']="exponential"
        a['rate']  = x[0]
        if(len(y) == 0):
            a['midpoint']=x[1]
        else:
            a['midpoint']=y[0]
        a['scale']=x[2]
    
    if(flag == 2):
        string3=re.compile('[A-Za-z]+[-](\d+[.]\d+)')
        y=string3.findall(expr)
        string2=re.compile('[-]?\d+[.]\d+')
        x=string2.findall(expr)
        a['type']="sigmoid"
        a['rate']  = x[0]
        if(len(y) == 0):
            a['midpoint']=x[1]
        else:
            a['midpoint']=y[0]
        a['scale']=x[2]
    if(flag == 3):
        string3=re.compile('[A-Za-z]+[-](\d+[.]\d+)')
        y=string3.findall(expr)
        string2=re.compile('[-]?\d+[.]\d+')
        x=string2.findall(expr)
        if(x[1] == x[3] and x[2] == x[4]):
            a['type'] = "exp_linear"
            a['rate'] = x[0]
            if(len(y) == 0):
                a['midpoint']=x[1]
            else:
                a['midpoint']=y[0]
            a['scale'] = x[2]
        else:
            a['type'] = "generic"
    if(flag == 4):
        a['type'] = "generic"
    
    return a
    
         
    return expr

def substituteconstant(a,b,d):
    result=[]
    for key1 in d:
        operatorindex=[]
        expr=d[key1]
        newvars=[t for t in re.split('[+/%)(*-]',expr) if t!='']
        operator = '[+/%)(*-]'
        index=0
        for c in expr:
            j=0
            if c not in re.split('[+/%)(*-]',expr) and c in operator:
                operatorindex.append(str(index))
                j+=1
            index+=1
        res=combineboth(operatorindex,newvars,expr,b)
        result.append(res)
    
    return result


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