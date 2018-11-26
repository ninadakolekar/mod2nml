from util import feedData
from lexer import lexer


def translatorWrapper(data,template,outFilename):
  output = open(outFilename,"w")
  output.write(feedData(template,data))

def translator(dataFile,verbose):
  tokens = lexer(dataFile,verbose)
  translatorWrapper(tokens,"channel_template.nml","output.nml")
  
if __name__=="__main__":
    translator("../examples/mod/K_HH.mod",True)