import bencodepy


# This just creates a bunch of of files with raw bencode data
# of primitive data values (sngle integar, a list of ints, a list of strings
# an object and a nested object.
# 
# (ps: also usefull to feed a fuzzer.)

i = 0
def writeSimple(val):
    global i
    f = open("examples/ex-{}".format(i), "wb")
    i = i + 1
    data = bencodepy.encode(val)
    f.write(data)
    f.close()


writeSimple(1)
lst = [1,2,3]
writeSimple(lst)
writeSimple(["a","b",3])
d = { "hello": "world"}
writeSimple(d)
writeSimple({ "list": lst, "yes": d})

