# Deism
![image](https://github.com/julianfl0w/Deism/assets/8158655/e8640f62-09af-40e2-913a-39a3ad2b818b)

## Introduction

Welcome to the official repository of the Deist religion, a unique faith that celebrates the existence of a singular God, transcendent and beyond the confines of our universe. This monorepo contains all the necessary code and documents that underpin the digital presence and operations of our religious community.

For more information, visit our [website](https://deism.church).

## Glossary

- **Deism**: The philosophical belief in a single, detached God who does not intervene in the universe.
- **The Book of Doctrine**: The foundational text of Deism, outlining its core principles across eight pillars: Origins, Nature, God, Church, Ethics, Ritual, Wisdom, and Prophecy.
- **The Book of Saints**: Recognizes individuals who have made significant contributions to Deism, categorized into three levels of sainthood.
- **The Third Testament**: An expanded canon that includes the Book of Doctrine and the Book of Saints, serving as the religious text for modern Deists.
- **Church of God (Deist)**: The governing body responsible for the teachings and administration of Deism.
- **DeismU**: The educational branch of the Church, offering courses and degrees on Deist principles.
- **Dena**: A digital currency managed by the Church, symbolizing economic stability and communal support.

# How to Contribute to Doctrine
![image](https://github.com/julianfl0w/Deism/assets/8158655/6fce52f2-1e46-43e9-a5b0-90f9549fb8cd)

To contribute to the Church's doctrine:

1. Fork this repository.
2. Make changes to the JSON-style Python files within the "Book of Doctrine" folder.
3. Submit a pull request for review.

# How to Contribute to the Website
![image](https://github.com/julianfl0w/Deism/assets/8158655/b21f8c44-104f-4c40-aae6-76e24b0bf3f9)

Our project's website, [deism.church](https://deism.church), serves as the primary digital platform for disseminating information about Deism. A significant portion of this monorepo is dedicated to the site's functionality. The repository uses AWS CodePipeline for continuous integration and delivery. Upon pushing updates to the "canon" branch, `export.py` is executed, compiling all JSON files from the "Book of Doctrine" into a single file, `julian_flare.json`, which is then served to the website.

Employing the Fractal Book technique, documents within the "Book of Doctrine" are compiled into a single JSON file (`julian.json`), facilitating easy distribution and access via the static site. To contribute or test changes, run `python export.py` or `runExport.sh` (Docker) at the root directory. The export process is automated through AWS CodePipeline upon updates to the `canon` branch.

To assist with website development:

1. Fork this repository.
2. Update the HTML/CSS/JavaScript files in the `/src` folder as needed.
3. Submit a pull request for consideration.

Contributions that are accepted and merged qualify for canonization consideration.

## DeismU
![image](https://github.com/julianfl0w/Deism/assets/8158655/38e07f55-26ef-430f-8542-a3ae43f7d49c)
DeismU outlines a curriculum leading to a recognized degree and potential canonization. The system involves certificate verification and account management handled on a backend EC2 server. The relevant code resides in the `/deismu` subfolder. 

**TODO**: Set up the Coursera-verifying Lambda with proper authentication.

## Dena
![image](https://github.com/julianfl0w/Deism/assets/8158655/027f2ab0-8b43-42bb-bb47-712a74ac5bc0)

Dena, inspired by the Roman Denarius, aims to provide a stable economic symbol equivalent to a year's salary, anchored in real estate values.

**TODO**: Finalize the implementation details.

## Contact and Community

For questions, discussions, or further information, please reach out through [our community forum](https://deism.church/community) (**TODO**) or directly via the contact information provided on our website.

We encourage all contributors to adhere to our [Code of Conduct](https://deism.church/codeofconduct) (**TODO**) to maintain a respectful and inclusive environment.
