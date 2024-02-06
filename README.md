# Deism
## Introduction
This monorepo holds the code which operates the Deist religion. 

## Technical explanation
### Book of Doctrine
Using Fractal Book technique, the files in Book of Doctrine are converted to one large JSON file of all doctrine (see deism.church/julian.json). Run python export.py in the root folder to verify this process. The export process runs in AWS CodePipeline every time the main branch is modified. The static site downloads this file, and serves it as a Single Page Application (SPA). 
### DeismU
DeismU establishes a list of Courses which constitute a degree. Any person completing the requirements is eligable for canonization. This process requires certificate verification and account management in a backend EC2 server. The salient code is in deismu subfolder.
## Contribute
### Doctrine
To make contributions to Church doctrine, please submit a pull request on the JSON-style python files in Book of Doctrine folder
### Website
To make contributions to the website, please submit a pull request on the src folder

Any accepted pull request qualifies you for canonization
