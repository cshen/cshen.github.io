# Directory Overview

This directory contains the source code for a personal academic website for a professor. The website is built using a static site generator called `jemdoc`.

## Key Files

*   `index.html`: The main landing page of the website.
*   `project.html`: A page listing the professor's research projects.
*   `teaching.html`: A page with information about the professor's teaching activities.
*   `cshen_papers.pdf`: A PDF document listing the professor's publications.
*   `data/bibtex/`: A directory containing `.bib` files for the professor's publications.
*   `css/`: A directory containing the CSS files for styling the website.
*   `jemdoc.py`: A Python script for the `jemdoc` static site generator.
*   `cl.sh`: A shell script for building the website using `jemdoc`.
*   `cs.conf`: The configuration file for `jemdoc`.

## Usage

The website is built by running the `cl.sh` script. This script executes the `jemdoc.py` static site generator with the `cs.conf` configuration file. The `jemdoc.py` script processes `.jemdoc` files (which are not present in the directory) to generate the final HTML files.

To add a new publication, a new `.bib` file should be added to the `data/bibtex/` directory. The website would then need to be rebuilt using the `cl.sh` script.
