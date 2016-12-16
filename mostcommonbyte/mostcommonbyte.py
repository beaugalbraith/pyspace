#!/usr/bin/env python3
import sys
# from collections import defaultdict
from collections import Counter
def bytesFromFile(filename, chunksize=8192):
  with open(filename, 'rb') as fd:
    while True:
      chunk = fd.read(chunksize)
      if chunk:
        yield from chunk
      else:
        break

# d = defaultdict(int)
c = Counter()

for b in bytesFromFile(sys.argv[1]):
  c[hex(b)] += 1
  # print(hex(b))

for (i,v) in c.most_common():
    print("{} : {}".format(i,v))
