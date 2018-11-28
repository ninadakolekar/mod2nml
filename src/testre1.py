import re
def equationParser(expr):
    flag = 0
    string1=re.compile('[(]*[-]?\d+[.]\d+[)]*[*][e][x][p][(]*\w+[-][-]?\d+[.]\d+[)]*[/][-]?\d+[.]\d+[)]*')
    if(len(string1.findall(expr))!=0 and string1.findall(expr)[0] == expr):
        flag = 1
    else:
        string1=re.compile('[(]*[-]?\d+[.]\d+[)]*[/][e][x][p][(]*\w+[-][-]?\d+[.]\d+[)]*[/][-]?\d+[.]\d+[)]*[+][1][)]*')
        if(len(string1.findall(expr))!= 0 and string1.findall(expr)[0] == expr):
            flag = 2
        else:
            string1=re.compile('[(]*[-]?\d+[.]\d+[)]*[*][(]*[A-Za-z]+[-][-]?\d+[.]\d+[)]*[/][(]*[-]?\d+[.]\d+[)]*[/][(]*[1][-][e][x][p][(]*[-][(]*[A-Za-z]+[-][-]?\d+[.]\d+[)]*[/][(]*[-]?\d+[.]\d+[)]*')
            if(len(string1.findall(expr))!= 0 and string1.findall(expr)[0] == expr):
                flag = 3
            else:
                flag = 4
                print('generic')
    a = {}
    if(flag == 1):
        string3=re.compile('[A-Za-z][-](\d+[.]\d+)')
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
        string3=re.compile('[A-Za-z][-](\d+[.]\d+)')
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
        string3=re.compile('[A-Za-z][-](\d+[.]\d+)')
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
    
    print(a)
    
         
    return expr

if __name__=="__main__":
    equationParser("0.125*((x--2.2)/3.2)/(1-exp(-(x--2.2)/3.2))")