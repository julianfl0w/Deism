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

        # list the title, Book Of Julian
        self.outstring += "# " + directory + "\n"

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
                self.outstring += ":".join(os.path.split(directory)) + "\n"
                # add its title
                self.outstring += "## " + file.replace(".py", "") + "\n"
                with open(d, "r") as f:
                    print(d)
                    c = eval(f.read())
                    for paragraph in c:
                        self.outstring += self.paragraphToMarkdown(paragraph)

        # then do subdirectories
        for file in os.listdir(directory):
            d = os.path.join(directory, file)
            if os.path.isdir(d):

                print(file)
                print(ignore)
                if file in ignore:
                    print("ignoring " + file)
                    continue
                else:
                    print("processing dir " + file)

                self.appendDirectory(d, depth=depth + 1)

    def paragraphToMarkdown(self, paragraph):
        outstring = ""
        for sentence in paragraph:
            if type(sentence) == str:
                outstring += "<sup>" + str(self.verse) + "</sup> " + sentence + ". "
                self.verse += 1
            else:
                outstring += self.listRecurse(sentence)
        outstring += "\n"
        return outstring

    def listRecurse(self, content, depth=0):
        string = ""
        print(type(content))
        print(type(content) == str)
        if type(content) == str:
            string += "  " * depth
            string += "- "
            string += content + "\n"
        elif type(content) == list:
            for i in content:
                string += self.listRecurse(i, depth + 1)
                string += "\n"
        elif type(content) == dict:
            for k, v in content.items():
                string += "  " * depth
                string += "- "
                string += k
                string += "\n"
                string += self.listRecurse(v, depth + 1)
                string += "\n"
        else:
            die
        return string


if __name__ == "__main__":
    m = Markdown(os.path.join(here, "BookOfJulian"))

    with open("README.md", "w+") as f:
        f.write(m.outstring)
    os.system("mdpdf -o README.pdf README.md")
