# Code

## Table of Contents:

- [Overview](#overview)
  - [File Structure](#file-structure)

## Overview

### File Structure

The code base is written in Python and is available on GitHub. The file structure is as follows (the `.` directory is the root directory):

generated with `tree -a -I '__pycache__' -I '.git' -I '.vscode' -I '.venv' -I '.DS_Store' -I '.gitignore' -I '.gitattributes`:

```file
./
├── .data/
│   ├── aggregate.py
│   ├── csvConverter.py
│   ├── data.csv
│   ├── ngram/
│   ├── ngramDownloader.sh*
│   ├── sort.py
│   ├── wordCompresser*
│   ├── wordCompresser2*
│   ├── wordCompresser2.rs
│   ├── wordCompresser3*
│   ├── wordCompresser3.rs
│   ├── wordCompresser4.py
│   ├── wordCompresser5.py
│   └── wordCompresser.rs
├── data/
│   ├── ai.joblib
│   └── data.csv
├── docs/
│   ├── code.md
│   ├── data.md
│   └── idea.md
├── main.py
├── README.md
├── requirements.txt
└── src/
    ├── ai.py
    └── randomWord.py
```

- The `.data` directory contains the scripts used to generate the data for the project. The scripts are written in Python and Rust. The scripts are `aggregate.py`, `csvConverter.py`, `ngramDownloader.sh`, `sort.py`, `wordCompresser`, `wordCompresser2`, `wordCompresser2.rs`, `wordCompresser3`, `wordCompresser3.rs`, `wordCompresser4.py`, `wordCompresser5.py`, and `wordCompresser.rs`.
  see the [data documentation](data.md) for more information.)
- The `data` directory contains the data files used in the project theses are `ai.joblib` (a pre-trained model) and `data.csv` (a dataset).
- The `docs` directory contains the documentation for the project. The documentation is split into three files `code.md`, `data.md` and `idea.md`.
- The `src` directory contains the source code for the project. The source code is split into two files `ai.py` (responsible for the AI) and `randomWord.py` (responsible for the random word generation).
- The `main.py` file is the entry point for the project it is what is run when the project is executed with `python3 main.py`.
- The `README.md` file is the main documentation for the project. It contains a brief overview of the project, how to run the project, and where to find the other documentation.
- The `requirements.txt` file contains the dependencies for the project. These can be installed with `pip install -r requirements.txt`.
