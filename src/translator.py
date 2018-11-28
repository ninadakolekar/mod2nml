from util import feedData
from lexer import lexer

def translatorWrapper(data,template,outFilename):
  output = open(outFilename,"w")
  output.write(feedData(template,data))

def translate(dataFile,outFile,verbose,config):
  tokens = lexer(dataFile,verbose,config)
  template = ""
  if config['generic']:
    template = "generic_template.nml"
  else:
    template = "channel_template.nml"
  if outFile is None:
    translatorWrapper(tokens,template,"output.nml")
  else:
    translatorWrapper(tokens,template,outFile)

if __name__=="__main__":
    translate("../examples/mod/NaChannel_HH.mod",None,True,{'generic':False})