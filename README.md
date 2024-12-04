# School Lab - ETS Montreal - Master's Degree - MGL869

Autumn 2024

---

## Summary

This repository contains the code for the school lab of the MGL869 course at ETS Montreal.
The goal of this lab is to implement simple version of algorithms "logistic regression" and "random forest" to predict
bugs in software [Hive](https://hive.com/).
---

## Lesson

[MGL869-01 Sujets spéciaux I : génie logiciel (A2024)](https://www.etsmtl.ca/etudes/cours/mgl869-a24)

## Authors

- Léo FORNOFF [leo.fornoff.1@ens.etsmtl.ca]()
- William PHAN [william.phan.1@ens.etsmtl.ca]()
- Yannis OUAKRIM [yannis.ouakrim.1@ens.etsmtl.ca]()

## Supervisor

- Mohammed SAYAGH, Ph.D., AP

---

## Table of contents

- [Get started](#get-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Project structure](#project-structure)

## Get started

### Prerequisites

- Python 3.11 or 3.12
- Pip
- Virtualenv
- Jupyter Notebook
- Required packages (see [requirements.txt](requirements.txt))
- Git
- [Scitools Understand](https://scitools.com/)

### Installation

1. Clone the repository
2. Create a virtual environment and activate it ([doc](https://docs.python.org/3/library/venv.html))
3. Install the required packages

```bash
pip3 install -r requirements.txt
```

> Note: You may need to adapt according to your system

4. Adapte configuration file `config.ini` to your environment. Especially, you need to set the path to the `und`
   executable of Understand.
5. Run the Jupyter Notebook

```bash
jupyter notebook
```

6. Open the notebook 'run.ipynb' and run the cells

> First run will take a lot of time because it will clone the repo, download the dataset and run the analysis.

## Project structure

- `config.ini`: Configuration file used by `run.ipyynb` and packages
- `requirements.txt`: List of required packages
- `run.ipynb`: Jupyter Notebook to run the analysis
- `README.md`: This file
- `data/`: Directory all the data needed for the analysis
- `Hive/`: Python package containing the functions used to analyze hive git repository
- `IA_models/`: Python package containing the functions used to train and test the IA models
- `Jira/`: Python package containing the functions used to analyze the Jira data
- `labeled_metrics_output/`: Directory containing the output of the analysis of the metrics
- `Understand/`: Python package containing the functions used to analyze data with Understand