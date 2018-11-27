from util import feedData
from lexer import lexer

def translatorWrapper(data,template,outFilename):
  output = open(outFilename,"w")
  output.write(feedData(template,data))

def translate(dataFile,outFile,verbose):
  tokens = lexer(dataFile,verbose)
  if outFile is None:
    translatorWrapper(tokens,"channel_template.nml","output.nml")
  else:
    translatorWrapper(tokens,"channel_template.nml",outFile)

if __name__=="__main__":
    translate("../examples/mod/NaChannel_HH.mod",None,True)