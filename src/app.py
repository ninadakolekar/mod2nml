import argparse
import os.path

from translator import translate

def app():

    parser = argparse.ArgumentParser(description="*** MOD to NeuroML Translator ***")
    parser.add_argument("-i","--input", required=True,help="Input MOD file path", metavar="FILE",type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-o","--output",  required=False,help="Output file path", metavar="FILE",type=lambda x: is_valid_dest(parser, x))
    parser.add_argument("-v","--verbose",dest="verbose", help="increase output verbosity",action="store_true")
    args = parser.parse_args() 

    translate(args.input,args.output,args.verbose)

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The path %s does not exist." % arg)
    if not os.path.isfile(arg):
        parser.error("%s is not a file." % arg)
    return arg

def is_valid_dest(parser, arg):
    if os.path.dirname(arg) is not '' and not os.path.exists(os.path.dirname(arg)):
        parser.error("The path %s is invalid or does not exist." % arg)
    if os.path.isfile(arg):
        parser.error("%s already exists." % arg)
    return arg


if __name__=="__main__":
    app()