import os
import sys
import pkg_resources

here = os.path.dirname(os.path.abspath(__file__))

if True or "sinode" not in [pkg.key for pkg in pkg_resources.working_set]:
    sys.path = [os.path.join(here, "..", "sinode")] + sys.path
    DEV = True
else:
    DEV = False


def copyDictUnique(indict, modifier):
    outdict = {}
    if type(indict) == dict:
        for k, v in indict.items():
            outdict[k + modifier] = copyDictUnique(v, modifier)
        return outdict
    else:
        return indict + modifier


import sinode.sinode as sinode
import copy

m = sinode.Category(directory = "Book Of Julian", depth = 1, parent = None)
#m.toGraphViz()
with open("README.md", 'w+') as f:
    f.write(m.toMarkdown())



