import os
import bencodepy
import pprint

fname = "../../examples/m0.bbmsg"

file = open(fname, "rb")

fileSize = os.path.getsize(fname)
input = file.read(fileSize) 

entry = bencodepy.decode(input)

print("Length of entry: {}".format(len(entry)))

print("length payload : {}".format(len(entry[0])))

pp = pprint.PrettyPrinter(indent=4, width=160)
pp.pprint(entry)
