import os
import json 

import Appendix
import Church
import Ethics
import God
import Introduction
import Nature
import Origins
import Prophesy
import Ritual
import Wisdom


def py2html(contents):
    htmlout = ""
    if os.path.isdir(indir):
        files = os.listdir(indir)
        pyfiles = [f for f in files if f.endswith(".py")]
        print(pyfiles)

        
        #children.sort(key=lambda x: x.meta["priority"], reverse=False)

if __name__ == "__main__":
    for k, v in vars(Origins).items():
        if not k.startswith("__"):
            print(k)