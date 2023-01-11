import sys
import os
import sinode
here = os.path.dirname(os.path.abspath(__file__))


class Markdown(sinode.Sinode):
    def __init__(self, rootdir):
        sinode.Sinode.__init__(self)
        self.content = []
        self.outstring = ""
        # recursively iterate through the directories
        self.appendDirectory(rootdir, depth=0)

    def appendDirectory(self, directory, depth):
        # first, do files at this level
        for file in os.listdir(directory):
            d = os.path.join(directory, file)

            # if it's a python file, execute it
            if not os.path.isdir(d) and d.endswith(".py"):
                with open(d, 'r') as f:
                    print(d)
                    c = eval(f.read())
                    self.outstring += self.toMarkdown(c, depth = 0)
        # then do subdirectories
        for file in os.listdir(directory):
            d = os.path.join(directory, file)
            if os.path.isdir(d):
                self.appendDirectory(d, depth=depth+1)

    def toMarkdown(self, content, depth):
        string = ""
        print(type(content))
        print(type(content) == str)
        if type(content) == str:
            string += content + "\n"
        elif type(content) == list:
            for i in content:
                string += "- "
                string += self.toMarkdown(i, depth + 1)
        elif type(content) == dict:
            for k, v in content.items():
                string += k + "\n"
                string += self.toMarkdown(v, depth + 1)
        return string

if __name__ == "__main__":
    m = Markdown("BookOfJulian")
    
    with open("README.md", 'w+') as f:
        f.write(m.outstring)
    os.system("mdpdf -o README.pdf README.md")
    