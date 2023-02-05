import os
import sys
import pkg_resources
import json
from bs4 import BeautifulSoup as bs

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
        "noPropagate": {},
        "font": {"color": "white"},
        "relationship": "descends",
        "engine": "dot",
        "graphParams": {
            "rankdir": "TB",
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
            "rankdir": "TB",
            "shape": "box",
            "penwidth": 0,
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
    skipGraphs=False,
    displayVerseNo=True,
)

print(m.toTableOfContents)

out = m.toMarkdown()
htmlString = out["html"]
soup = bs(htmlString)
htmlString = soup.prettify()

with open("ABSA.html", "w+") as f:
    f.write(htmlString)
with open("README.md", "w+") as f:
    f.write(out["markdown"])

# m.toPDF()
