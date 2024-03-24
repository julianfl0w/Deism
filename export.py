import os
import sys
import pkg_resources
import json
from bs4 import BeautifulSoup as bs

here = os.path.dirname(os.path.abspath(__file__))
os.makedirs("build", exist_ok=True)
os.makedirs("build/graphs", exist_ok=True)

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

lineColor = "#00ffff"
lineColor = '"#88ffff"'
# "color": "black",
# "color": "\"#262626\"",

m = fractal_book.FractalBook(
    meta={
        "priority": 1000,
        "ignore": False,
        "type": "default",
        "topology": "nested",
        "noPropagate": {},
        "font": {"color": "white"},
        "relationship": "descends",
        "engine": "dot",
        "graphParams": {
            "rankdir": "TB",
            "style": "filled",
            "fontcolor": "black",
            "color": "black",
            # "color": "\"#262626\"",
            "bgcolor": "white",
            # "fillcolor": "\"darkgray:gold\"",
            "gradientangle": 0,
            "dpi": 300,
        },
        "boxParams": {
            "rankdir": "TB",
            "shape": "box",
            "penwidth": 1,
            "color": lineColor,
            "fontcolor": "black",
            # "fillcolor": "\"darkorchid4:grey10\"",
            "fillcolor": "white",
            "style": "filled",
            "gradientangle": 270.05,
        },
        "arrowParams": {"color": lineColor, "penwidth": 1},
    },
    origin="directory",
    buildDir="build",
    graphsDir="graphs",
    source="Book Of Doctrine",
    depth=1,
    parent=None,
    skipGraphs=False,
    displayVerseNo=True,
    align="left"
)

m.dump()

os.system("cp -r src/* build/")

os.system("rm -rf src/book_of_doctrine")
os.system("rm src/book_of_doctrine.html")
os.system("cp -r src/* build/")
with open("./src/index_template.html") as f:
    template = f.read()
julian_flare = json.dumps(m.exportStatic(template=template, buildDir = "./build"), indent=2)

with open("build/julian_flare.json", "w+") as f:
    f.write(julian_flare)

# for testing from the src folder
with open("src/julian_flare.json", "w+") as f:
    f.write(julian_flare)

os.system('cp -r "build/book_of_doctrine" "src/book_of_doctrine"')
os.system('cp "build/index.html" "src/index.html"')

with open("build/julian.json", "w+") as f:
    f.write(json.dumps(m.asDict(), indent=2))

# print(m.toTableOfContents)

out = m.toMarkdown(textColor="black")
htmlString = out["html"]
soup = bs(htmlString, features="lxml")
htmlString = soup.prettify()

with open("build/ABSA.html", "w+") as f:
    f.write(htmlString)
with open("build/README.md", "w+") as f:
    f.write(out["markdown"])

os.system("cp -r build/graphs src")
# m.toPDF()
