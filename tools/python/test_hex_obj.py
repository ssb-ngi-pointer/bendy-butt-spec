import sys
import codecs
import bencodepy
import pprint



data = ""

if len(sys.argv) == 2:
    data = sys.argv[1]
else:
    print("reading from stdin")
    data = input()

# assuming all input is hex encoded
dataBytes = codecs.decode(data, 'hex_codec')

print("decoding {} bytes of data".format(len(dataBytes)))

transferObj = bencodepy.decode(dataBytes)

pp = pprint.PrettyPrinter(indent=4, width=160)
pp.pprint(transferObj)
