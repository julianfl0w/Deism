import os
import sys
import pkg_resources
import json

here = os.path.dirname(os.path.abspath(__file__))

if True or "sinode" not in [pkg.key for pkg in pkg_resources.working_set]:
    sys.path = [os.path.join(here, "..", "sinode")] + sys.path
    DEV = True
else:
    DEV = False
import sinode.fractal_book as fractal_book


def copyDictUnique(indict, modifier):
    outdict = {}
    if type(indict) == dict:
        for k, v in indict.items():
            outdict[k + modifier] = copyDictUnique(v, modifier)
        return outdict
    else:
        return indict + modifier


import copy

m = fractal_book.FractalBook(
    meta={
        "priority": 1000,
        "ignore": False,
        "type": "default",
        "font": {"color": "white"},
        "relationship": "descends",
        "engine": "dot",
        "graphParams": {
            "rankdir": "LR",
            "style": "filled",
            "fontcolor": "white",
            "color": "white",
            # "color": "\"#262626\"",
            "bgcolor": '"#262626"',
            # "fillcolor": "\"darkgray:gold\"",
            "gradientangle": 0,
            "dpi": 300,
        },
        "boxParams": {
            "rankdir": "LR",
            "shape": "box",
            # "color": "black",
            # "color": "\"#262626\"",
            "color": "black",
            "fontcolor": "white",
            # "fillcolor": "\"darkorchid4:grey10\"",
            "fillcolor": '"#6C2944:#29001C"',
            "style": "filled",
            "gradientangle": 270.05,
        },
        "arrowParams": {"color": "white", "penwidth": 1},
    },
    origin="directory",
    source="Book Of Julian",
    depth=0,
    parent=None,
)

print(m.toTableOfContents)

with open("README.md", "w+") as f:
    f.write(m.toMarkdown()["markdown"])

# m.toPDF()
