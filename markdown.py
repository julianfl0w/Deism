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
        print("INDIR " + directory)

        # read in ignore file
        if os.path.exists(os.path.join(directory, "ignore.py")):
            with open(os.path.join(directory, "ignore.py"), "r") as f:
                ignore = eval(f.read())
        else:
            ignore = []

        print("Ignore " + str(ignore))

        # first, do files at this level
        for file in os.listdir(directory):

            d = os.path.join(directory, file)

            # if it's a python file, execute it
            # each python file is a chapter, containing a list of paragraphs
            if not os.path.isdir(d) and d.endswith(".py"):

                if file in ignore or file == "ignore.py":
                    continue
                else:
                    print("processing file " + file)

                self.verse = 0
                # add its path
                self.outstring += ":".join(str(directory).split(os.sep)[5:]) + "\n"
                # add its title
                self.outstring += "## " + file.replace(".py", "") + "\n"
                with open(d, "r") as f:
                    print(d)
                    chapter = eval(f.read())
                    for i, paragraph in enumerate(chapter):
                        if type(paragraph) == dict:
                            if (
                                "meta" in paragraph.keys()
                                and paragraph["meta"]["type"] == "lineage"
                            ):
                                self.outstring += self.toGraph(
                                    paragraph, name=paragraph["meta"]["name"]
                                )
                                
                            else:
                                self.outstring += self.listToMarkdown(paragraph)
                                

                        else:
                            self.outstring += self.paragraphToMarkdown(paragraph)
                        # add a new line between paragraphs
                        self.outstring += "\n\n"

        # then do subdirectories
        for file in os.listdir(directory):
            d = os.path.join(directory, file)
            if os.path.isdir(d):

                if file in ignore:
                    print("ignoring " + file)
                    continue
                else:
                    print("processing dir " + file)

                self.appendDirectory(d, depth=depth + 1)

    def paragraphToMarkdown(self, paragraph):
        outstring = ""
        if type(paragraph[0]) == str:
            for sentence in paragraph:
                if type(sentence) == str:
                    outstring += "<sup>" + str(self.verse) + "</sup> " + sentence + ". "
                    self.verse += 1
                else:
                    outstring += self.listToMarkdown(sentence)
        return outstring

    def listToMarkdown(self, content, depth=0):
        string = ""
        print(type(content))
        print(type(content) == str)
        if type(content) == str:
            string += "  " * depth
            string += "- "
            string += content + "\n"
        elif type(content) == list:
            for i in content:
                string += self.listToMarkdown(i, depth + 1)
            # string += "\n"
        elif type(content) == dict:
            for k, v in content.items():
                if k == "meta":
                    continue
                string += "  " * depth
                string += "- "
                string += k
                string += "\n"
                string += self.listToMarkdown(v, depth + 1)
        elif content is None:
            pass
        else:
            print(type(content))
            die
        return string

    def toGraphRecurse(self, content, parent=None):
        string = ""
        if type(content) == str:
            string += "'" + content + "' [shape=box]\n"
        elif type(content) == list:
            raise Exception("Lists not permitted")
        elif type(content) == dict:
            for k, v in content.items():
                print("Processing " + k)
                # dont record meta block
                if k == "meta":
                    continue

                # create this key
                keyWithQuotes = '"' + k + '"'
                print(keyWithQuotes)
                string += keyWithQuotes + " [shape=box, color = cadetblue1]\n"
                string += self.toGraphRecurse(v, parent=keyWithQuotes)
                # relationships
                if parent is not None:
                    string += parent + " -> " + keyWithQuotes + " [penwidth=1]\n"

        return string

    def toGraph(self, content, name):
        print("graphing")
        dotString = ""
        dotString += "digraph D {\n"
        dotString += self.toGraphRecurse(content)
        dotString += "}"
        
        filename = os.path.join("graphs", name.replace(" ", "_") + ".dot")
        with open(filename, "w+") as f:
            f.write(dotString)
        
        imagename = os.path.join("graphs", name.replace(" ", "_") + ".png")
        runstring = "dot -Tpng \'" + filename + "\' -o " + "\'" + imagename + "\'"
        print(runstring)
        os.system(runstring)
        
        retString = "\n![" + name + "](/" + imagename + "?raw=true \"" + name + "\")\n\n"

        return retString


if __name__ == "__main__":
    m = Markdown(os.path.join(here, "BookOfJulian"))

    preformat = m.outstring
    preformat = preformat.replace("/graphs", os.path.join(here, "graphs"))
    preformat = preformat.replace("?raw=true", "")
    
    with open("README.md", "w+") as f:
        f.write(preformat)
    os.system("mdpdf -o README.pdf README.md")
