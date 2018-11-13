from util import feedData
from lexer import lexer


# Call as  gate['instances'] = str(countInstances(breakpointBlock,state))
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

def translatorWrapper(data,template,outFilename):
  output = open(outFilename,"w")
  output.write(feedData(template,data))

def translator(dataFile):
  translatorWrapper(lexer(dataFile,False),"template.nml","output.nml")
  
if __name__=="__main__":
    translator("../examples/mod/KCa_Channel.mod")